"""
Sky Credit Group Voice Assistant using DSPy
A modular approach to ensure strict instruction following and step-by-step execution.
"""

import dspy
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger_config import get_logger
logger = get_logger("main_agent")

# Import from our modules
from .core_modules import (
    GreetingModule,
    VerificationModule,
    ClosingModule
)
from .scenarios import (
    AccountBalanceModule
)

@dataclass
class ConversationState:
    """Tracks the current state of the conversation"""
    customer_data: Optional[Dict] = None
    verified: bool = False
    scenario_type: Optional[str] = None
    conversation_history: List[str] = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []


class MainAgent(dspy.Module):
    """Main agent orchestrator for the Sky Credit voice assistant"""
    
    def __init__(self):
        super().__init__()
        self.greeting_module = GreetingModule()
        self.verification_module = VerificationModule()
        self.account_balance_module = AccountBalanceModule()
        self.closing_module = ClosingModule()
        
        # Initialize conversation state
        self.state = ConversationState()
        self.verification_data = {}  # Store verification info as we collect it
        self.actions_taken = []  # Track actions for closing summary
    
    def start_conversation(self):
        """Start the conversation with greeting"""
        logger.info("Starting conversation: greeting")
        greeting = self.greeting_module()
        self.state.conversation_history.append(f"Assistant: {greeting}")
        return greeting
    
    def process_customer_input(self, customer_input: str):
        """Process customer input and determine next action"""
        logger.info(f"Received customer input: {customer_input}")
        self.state.conversation_history.append(f"Customer: {customer_input}")
        
        # If not verified yet, handle verification
        if not self.state.verified:
            verification_response = self._handle_verification(customer_input)
            # After verification completes, go straight to account balance scenario
            if self.state.verified:
                logger.info("Verification complete. Starting account balance scenario")
                self.state.scenario_type = "account_balance"
                return self._handle_scenario_step(customer_input)
            return verification_response
        
        # If we have a scenario in progress, continue it
        if self.state.scenario_type and self.state.scenario_type != "closing":
            return self._handle_scenario_step(customer_input)
        
        # Default to account balance scenario
        self.state.scenario_type = "account_balance"
        return self._handle_scenario_step(customer_input)
    
    def _handle_verification(self, customer_input: str):
        """Handle the verification process using DSPy"""
        # Use DSPy to handle verification
        result = self.verification_module(
            customer_input=customer_input,
            verification_data=self.verification_data
        )
        
        # Update verification data with new info
        self.verification_data.update(result['updated_data'])
        
        # Check if verification is complete
        if result['verification_complete']:
            lookup_result = self.verification_module.lookup_customer_data(self.verification_data)
            
            if lookup_result['customer_found']:
                self.state.customer_data = lookup_result['customer_data']
                self.state.verified = True
                logger.info("Customer verified: %s %s", self.state.customer_data.get('firstName'), self.state.customer_data.get('lastName'))
            else:
                logger.warning("Customer lookup failed")
        
        response = result['response']
        self.state.conversation_history.append(f"Assistant: {response}")
        return response
        
    def _handle_scenario_step(self, customer_response: str):
        """Handle current scenario step"""
        conversation_history = "\n".join(self.state.conversation_history[-5:])
        
        if self.state.scenario_type == "account_balance":
            # Ensure we have customer data before proceeding
            if not self.state.customer_data:
                logger.warning("Account balance requested but customer_data missing")
                return "I apologize, but I need to verify your account first. Let me transfer you to an agent."
            
            result = self.account_balance_module(
                customer_data=self.state.customer_data,
                customer_input=customer_response,
                conversation_history=conversation_history
            )
            
            response = result['response']
            logger.info("Account balance response generated")
            
            # Track that we handled the account balance request
            if "account_balance" not in [action.split()[1] for action in self.actions_taken if "Handled" in action]:
                self.actions_taken.append("Handled account_balance request")
            
            # Check if this response is asking "anything else" - if so, it's the closing
            if "anything else" in response.lower() and "assist" in response.lower():
                self.state.conversation_history.append(f"Assistant: {response}")
                return self._start_closing()
            
            # Otherwise, continue the account balance conversation
            
        else:
            # For other scenarios, let DSPy handle them or provide fallback
            response = "I understand your request. Let me help you with that."
            self.actions_taken.append(f"Handled {self.state.scenario_type} request")
            return self._start_closing()
        
        self.state.conversation_history.append(f"Assistant: {response}")
        return response
    
    def _start_closing(self):
        """Start the closing process"""
        self.state.scenario_type = "closing"
        actions_summary = "; ".join(self.actions_taken) if self.actions_taken else "Provided account information"
        
        # Let DSPy handle the closing
        conversation_history = "\n".join(self.state.conversation_history[-5:])
        logger.info("Starting call closing")
        result = self.closing_module(
            actions_summary=actions_summary,
            step=1,  # Start closing
            customer_response=""
        )
        
        response = result['response']
        self.state.conversation_history.append(f"Assistant: {response}")
        return response
