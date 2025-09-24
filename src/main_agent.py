import dspy
from typing import Optional
from dataclasses import dataclass
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger_config import get_logger
logger = get_logger("main_agent")

from .core_modules import SkyCreditVoiceAssistant, lookup_customer_tool

@dataclass
class ConversationState:
    history: Optional[dspy.History] = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = dspy.History(messages=[])

class MainAgent:
    """Main Agent Class"""
    
    def __init__(self):
        self.lookup_tool = dspy.Tool(lookup_customer_tool, name="lookup_customer", desc="Look up customer account information")
        
        self.agent = dspy.ReAct(
            SkyCreditVoiceAssistant,
            tools=[self.lookup_tool]
        )
        
        self.state = ConversationState()
        logger.info("MainAgent initialized with DSPy ReAct")
    
    def process_input(self, customer_input: str):
        """Process customer input"""
        logger.info(f"Processing input: {customer_input}")
        
        # Generate response from the agent
        result = self.agent(
            customer_input=customer_input,
            history=self.state.history
        )

        logger.info(f"Generated Result: {result}")
        
        # Log if tools were used
        if hasattr(result, 'tool_outputs') and result.tool_outputs:
            logger.info(f"🔧 DSPy Tool Used: {len(result.tool_outputs)} tool calls made")
            for i, output in enumerate(result.tool_outputs):
                logger.info(f"   Tool {i+1} output: {output[:100]}..." if len(output) > 100 else f"   Tool {i+1} output: {output}")
        
        response = result.response
        
        # Add interaction to history
        self.state.history.messages.append({
            "customer_input": customer_input,
            "response": response
        })
        
        logger.info(f"DSPy History now has {len(self.state.history.messages)} messages")
        
        return response
    
    def get_history(self):
        """Get DSPy history as string by capturing inspect_history output"""
        import io
        import sys
        from contextlib import redirect_stdout
        
        # Capture the printed output from dspy.inspect_history()
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            dspy.inspect_history(n=100)
        return captured_output.getvalue()
