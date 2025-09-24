"""
Testing Agent for Sky Credit Voice Assistant
Simulates customer interactions using an LLM instead of hardcoded responses.
"""

import dspy
from typing import Optional, List
import json
from logger_config import get_logger

# Use unified app logger
logger = get_logger("testing_agent")

class TestingAgentSignature(dspy.Signature):
    """Testing agent that simulates a customer calling Sky Credit Group"""
    scenario_context: str = dspy.InputField(desc="Customer details and scenario information")
    conversation_history: str = dspy.InputField(desc="Previous conversation messages")
    assistant_message: str = dspy.InputField(desc="Latest message from the assistant")
    
    customer_response: str = dspy.OutputField(desc="Natural customer response as Paul Walshe")
    should_end_call: bool = dspy.OutputField(desc="True if conversation objective is complete and should end")

class TestingAgent:
    """Agent that simulates customer interactions for testing the voice assistant"""
    
    def __init__(self):
        logger.debug("Initializing TestingAgent")
        self.testing_agent = dspy.ChainOfThought(TestingAgentSignature)
        self.conversation_history = []
        self.conversation_ended = False
        logger.debug("TestingAgent initialized successfully")
        
        # Customer scenario details
        self.scenario_context = """
You are Paul Walshe, a customer calling Sky Credit Group to check your account balance.

Your details:
- Reference number: XT59591
- First name: Paul
- Last name: Walshe  
- Date of birth: 15th March 1985

Follow these steps naturally in conversation:
1. Ask for your account balance
2. Provide reference number XT59591 when asked
3. Provide first name Paul when asked
4. Provide last name Walshe when asked
5. Provide date of birth 15th March 1985 when asked
6. Confirm payment details when asked
7. End conversation when you have received all information

Instructions:
- Be conversational and natural, like a real customer
- Only provide information when specifically asked for it
- Don't rush through all steps at once - let the conversation flow naturally
- Stay in character as Paul Walshe throughout the conversation
"""
    
    def get_initial_message(self) -> str:
        """Get the initial customer message to start the conversation"""
        logger.debug("Getting initial customer message")
        return "Hello"
    
    def generate_response(self, assistant_message: str) -> Optional[str]:
        """Generate customer response to assistant message"""
        if self.conversation_ended:
            return None

        # Add assistant message to history
        self.conversation_history.append(f"Assistant: {assistant_message}")

        # Create conversation history string
        history_str = "\n".join(self.conversation_history[-10:])  # Last 10 messages

        try:
            result = self.testing_agent(
                scenario_context=self.scenario_context,
                conversation_history=history_str,
                assistant_message=assistant_message
            )

            if result.should_end_call:
                logger.info("Testing agent ending conversation")
                self.conversation_ended = True
                return None

            # Add customer response to history
            customer_response = result.customer_response
            self.conversation_history.append(f"Customer: {customer_response}")

            return customer_response

        except Exception as e:
            logger.error(f"Testing Agent error: {str(e)}")
            return "Could you please repeat that?"
    
    def is_conversation_ended(self) -> bool:
        """Check if the conversation has ended"""
        return self.conversation_ended
    
    def reset_conversation(self):
        """Reset conversation for new test"""
        self.conversation_history = []
        self.conversation_ended = False

class ConversationEvaluator:
    """Evaluates conversation against expected outcomes"""
    
    def __init__(self):
        logger.debug("Initializing ConversationEvaluator")
        self.evaluation_agent = dspy.ChainOfThought(
            "conversation_transcript, expected_outcomes -> evaluation_json: str"
        )

        self.expected_outcomes = [
            "The main agent should ask for the customer's reference number",
            "The main agent should ask for the customer's first name",
            "The main agent should ask for the customer's last name",
            "The main agent should ask for the customer's date of birth",
            "The main agent should state that they are looking up the account",
            "The main agent should state that the account has been located and provide the current net balance",
            "The main agent should state the next payment amount and its due date",
            "The main agent should ask if the payment will be taken successfully on the due date",
            "The main agent should confirm that the payment will process automatically",
            "The main agent should ask if there is anything else and thank the caller"
        ]
        logger.debug(f"Initialized with {len(self.expected_outcomes)} expected outcomes")
    
    def evaluate_conversation(self, conversation_transcript: List[str]) -> dict:
        """Evaluate the conversation against expected outcomes"""
        logger.info(f"Evaluating conversation with {len(conversation_transcript)} messages")

        transcript_str = "\n".join(conversation_transcript)
        outcomes_str = "\n".join([f"{i+1}. {outcome}" for i, outcome in enumerate(self.expected_outcomes)])

        try:
            result = self.evaluation_agent(
                conversation_transcript=transcript_str,
                expected_outcomes=outcomes_str
            )

            # Try to parse the JSON response
            evaluation = json.loads(result.evaluation_json)
            logger.info(f"Evaluation completed")
            return evaluation

        except Exception as e:
            logger.error(f"Evaluation error: {str(e)}")
            return {"error": f"Failed to evaluate conversation: {str(e)}"}
