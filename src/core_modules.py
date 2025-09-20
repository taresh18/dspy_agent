"""
Core modules for Sky Credit Voice Assistant
Contains greeting, verification, closing and other core functionality.
"""

import dspy
import json
from typing import Dict
from .db import lookup_customer

# Core DSPy Signatures
class GreetingSignature(dspy.Signature):
    """Generate the initial greeting for Sky Credit Group voice assistant"""
    response: str = dspy.OutputField(desc="Greeting message following exact script: 'Thank you for calling the Sky Credit Group. My name is Jess, an automated AI voice assistant. Can I please have your name, and find out how I can assist you today?'")

class VerificationHandlerSignature(dspy.Signature):
    """Handle Sky Credit Group verification. Collect: reference number, first name, last name, date of birth."""
    customer_input: str = dspy.InputField(desc="Customer's current response")
    verification_data: str = dspy.InputField(desc="Already collected data as JSON: {reference_or_mobile, first_name, last_name, date_of_birth}")
    
    response: str = dspy.OutputField(desc="What to ask customer next or confirmation message")
    updated_data: str = dspy.OutputField(desc="Updated verification data as JSON with any new info extracted")
    is_complete: bool = dspy.OutputField(desc="True only if all 4 items collected: reference_or_mobile, first_name, last_name, date_of_birth")

class CustomerLookupSignature(dspy.Signature):
    """Look up customer in database using collected verification info"""
    reference_number: str = dspy.InputField(desc="Customer reference number or mobile number")
    first_name: str = dspy.InputField(desc="Customer first name")
    last_name: str = dspy.InputField(desc="Customer last name")
    
    customer_found: bool = dspy.OutputField(desc="Whether customer was found in database")
    customer_data: str = dspy.OutputField(desc="Customer account information as JSON string")

class ClosingSignature(dspy.Signature):
    """Handle the mandatory closing checklist"""
    actions_summary: str = dspy.InputField(desc="Summary of actions taken during the call")
    step_number: int = dspy.InputField(desc="Current closing step (1-4)")
    customer_response: str = dspy.InputField(desc="Customer's response")
    
    response: str = dspy.OutputField(desc="Closing response following mandatory steps")
    next_step: int = dspy.OutputField(desc="Next closing step")
    call_complete: bool = dspy.OutputField(desc="Whether the call is complete")

# Core DSPy Modules
class GreetingModule(dspy.Module):
    """Module for handling initial greeting"""
    
    def __init__(self):
        super().__init__()
        self.greeting = dspy.Predict(GreetingSignature)
    
    def forward(self):
        result = self.greeting()
        return result.response

class VerificationModule(dspy.Module):
    """Module for handling customer verification"""
    
    def __init__(self):
        super().__init__()
        self.verify = dspy.ChainOfThought(VerificationHandlerSignature)
    
    def forward(self, customer_input: str, verification_data: dict):
        result = self.verify(
            customer_input=customer_input,
            verification_data=json.dumps(verification_data)
        )
        
        # Parse updated data
        try:
            updated = json.loads(result.updated_data) if result.updated_data else {}
        except:
            updated = {}
        
        return {
            "response": result.response,
            "updated_data": updated,
            "verification_complete": result.is_complete
        }
    
    def lookup_customer_data(self, verification_data: dict):
        """Look up customer after verification is complete"""
        ref = verification_data.get('reference_or_mobile', '')
        fname = verification_data.get('first_name', '')
        lname = verification_data.get('last_name', '')
        
        customer = lookup_customer(ref, fname, lname)
        if customer:
            return {
                "customer_found": True,
                "customer_data": customer
            }
        return {
            "customer_found": False,
            "customer_data": None
        }

class ClosingModule(dspy.Module):
    """Module for handling call closing"""
    
    def __init__(self):
        super().__init__()
        self.closing = dspy.Predict(ClosingSignature)
    
    def forward(self, actions_summary: str, step: int, customer_response: str = ""):
        result = self.closing(
            actions_summary=actions_summary,
            step_number=step,
            customer_response=customer_response
        )
        
        return {
            "response": result.response,
            "next_step": result.next_step,
            "call_complete": result.call_complete
        }
