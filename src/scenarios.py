"""
Customer service scenarios for Sky Credit Voice Assistant
Contains DSPy signatures and modules for specific customer service scenarios.
"""

import dspy
import json
from typing import Dict

class AccountBalanceSignature(dspy.Signature):
    """Handle account balance inquiry. Must provide: current balance, next payment amount, next payment date, ask about payment confirmation."""
    customer_data: str = dspy.InputField(desc="Customer account info as JSON with accountBalance, nextPaymentAmount, nextPaymentDate")
    customer_input: str = dspy.InputField(desc="What customer said")
    conversation_history: str = dspy.InputField(desc="Previous conversation")
    
    response: str = dspy.OutputField(desc="Assistant response providing account balance, next payment info, and asking about payment")
    scenario_complete: bool = dspy.OutputField(desc="True if balance inquiry is complete")
    needs_deferral: bool = dspy.OutputField(desc="True if customer needs payment deferral")

class ArrearsManagementSignature(dspy.Signature):
    """Handle arrears management scenario with mandatory steps"""
    customer_data: str = dspy.InputField(desc="Customer account information")
    step_number: int = dspy.InputField(desc="Current step in arrears management (1-8)")
    customer_response: str = dspy.InputField(desc="Customer's latest response")
    
    response: str = dspy.OutputField(desc="Assistant's response following the mandatory script")
    next_step: int = dspy.OutputField(desc="Next step number to execute")
    scenario_complete: bool = dspy.OutputField(desc="Whether arrears management is complete")

class PaymentDeferralSignature(dspy.Signature):
    """Handle payment deferral scenario with mandatory steps"""
    customer_data: str = dspy.InputField(desc="Customer account information")
    step_number: int = dspy.InputField(desc="Current step in payment deferral (1-6)")
    customer_response: str = dspy.InputField(desc="Customer's latest response")
    
    response: str = dspy.OutputField(desc="Assistant's response following the mandatory script")
    next_step: int = dspy.OutputField(desc="Next step number to execute")
    scenario_complete: bool = dspy.OutputField(desc="Whether payment deferral is complete")
    needs_transfer: bool = dspy.OutputField(desc="Whether customer needs transfer to hardship team")

class HardshipAssistanceSignature(dspy.Signature):
    """Handle hardship assistance scenario with mandatory steps"""
    customer_data: str = dspy.InputField(desc="Customer account information")
    step_number: int = dspy.InputField(desc="Current step in hardship assistance (1-7)")
    customer_response: str = dspy.InputField(desc="Customer's latest response")
    
    response: str = dspy.OutputField(desc="Assistant's response following the mandatory script")
    next_step: int = dspy.OutputField(desc="Next step number to execute")
    scenario_complete: bool = dspy.OutputField(desc="Whether hardship assistance is complete")
    needs_transfer: bool = dspy.OutputField(desc="Whether customer needs transfer to hardship team")

class BankingUpdateSignature(dspy.Signature):
    """Handle banking detail updates scenario with mandatory steps"""
    customer_data: str = dspy.InputField(desc="Customer account information")
    step_number: int = dspy.InputField(desc="Current step in banking update (1-10)")
    customer_response: str = dspy.InputField(desc="Customer's latest response")
    
    response: str = dspy.OutputField(desc="Assistant's response following the mandatory script")
    next_step: int = dspy.OutputField(desc="Next step number to execute")
    scenario_complete: bool = dspy.OutputField(desc="Whether banking update is complete")


class AccountBalanceModule(dspy.Module):
    """Module for handling account balance checks"""
    
    def __init__(self):
        super().__init__()
        self.balance_handler = dspy.ChainOfThought(AccountBalanceSignature)
    
    def forward(self, customer_data: Dict, customer_input: str, conversation_history: str):
        # Ensure required fields exist; add defaults so LM has structured input
        safe_data = {
            "firstName": customer_data.get("firstName"),
            "lastName": customer_data.get("lastName"),
            "accountBalance": customer_data.get("accountBalance"),
            "nextPaymentAmount": customer_data.get("nextPaymentAmount") or customer_data.get("minimumAmountDue"),
            "nextPaymentDate": customer_data.get("nextPaymentDate"),
        }
        result = self.balance_handler(
            customer_data=json.dumps(safe_data),
            customer_input=customer_input,
            conversation_history=conversation_history
        )
        
        return {
            "response": result.response,
            "scenario_complete": bool(getattr(result, "scenario_complete", False)),
            "needs_deferral": bool(getattr(result, "needs_deferral", False))
        }

class ArrearsManagementModule(dspy.Module):
    """Module for handling arrears management"""
    
    def __init__(self):
        super().__init__()
        self.arrears_management = dspy.Predict(ArrearsManagementSignature)
    
    def forward(self, customer_data: Dict, step: int, customer_response: str = ""):
        result = self.arrears_management(
            customer_data=json.dumps(customer_data),
            step_number=step,
            customer_response=customer_response
        )
        
        return {
            "response": result.response,
            "next_step": result.next_step,
            "scenario_complete": result.scenario_complete
        }

class PaymentDeferralModule(dspy.Module):
    """Module for handling payment deferrals"""
    
    def __init__(self):
        super().__init__()
        self.payment_deferral = dspy.Predict(PaymentDeferralSignature)
    
    def forward(self, customer_data: Dict, step: int, customer_response: str = ""):
        result = self.payment_deferral(
            customer_data=json.dumps(customer_data),
            step_number=step,
            customer_response=customer_response
        )
        
        return {
            "response": result.response,
            "next_step": result.next_step,
            "scenario_complete": result.scenario_complete,
            "needs_transfer": result.needs_transfer
        }

class HardshipAssistanceModule(dspy.Module):
    """Module for handling hardship assistance"""
    
    def __init__(self):
        super().__init__()
        self.hardship_assistance = dspy.Predict(HardshipAssistanceSignature)
    
    def forward(self, customer_data: Dict, step: int, customer_response: str = ""):
        result = self.hardship_assistance(
            customer_data=json.dumps(customer_data),
            step_number=step,
            customer_response=customer_response
        )
        
        return {
            "response": result.response,
            "next_step": result.next_step,
            "scenario_complete": result.scenario_complete,
            "needs_transfer": result.needs_transfer
        }

class BankingUpdateModule(dspy.Module):
    """Module for handling banking detail updates"""
    
    def __init__(self):
        super().__init__()
        self.banking_update = dspy.Predict(BankingUpdateSignature)
    
    def forward(self, customer_data: Dict, step: int, customer_response: str = ""):
        result = self.banking_update(
            customer_data=json.dumps(customer_data),
            step_number=step,
            customer_response=customer_response
        )
        
        return {
            "response": result.response,
            "next_step": result.next_step,
            "scenario_complete": result.scenario_complete
        }
