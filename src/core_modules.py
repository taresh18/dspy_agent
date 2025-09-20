import dspy
from typing import Dict, Optional
from .db import lookup_customer

def lookup_customer_tool(reference_or_mobile: str, first_name: str, last_name: str) -> str:
    """
    Look up customer account information using reference number/mobile and name verification.
    
    Args:
        reference_or_mobile: Customer reference number or mobile number
        first_name: Customer's first name
        last_name: Customer's last name
        
    Returns:
        String with customer information or error message
    """
    customer = lookup_customer(reference_or_mobile, first_name, last_name)
    
    if customer:
        return f"Customer found: {customer.firstName} {customer.lastName}. Account Balance: ${customer.accountBalance}, Next Payment: ${customer.minimumAmountDue} due {customer.nextPaymentDate}, Arrears: ${customer.arrearsBalance}, Days Past Due: {customer.daysPastDue}"
    else:
        return "Customer not found with provided details"

class SkyCreditVoiceAssistant(dspy.Signature):
    """
    You are Jess, an AI voice assistant for Sky Credit Group handling account inquiries and payment support.
    
    GREETING: "Thank you for calling the Sky Credit Group. My name is Jess, an automated AI voice assistant. Can I please have your name, and find out how I can assist you today?"
    
    MANDATORY VERIFICATION (collect ALL before using lookup_customer tool):
    - Customer reference number (or mobile if unknown)
    - First name  
    - Last name
    - Date of birth
    Then say "Thank you, I am just looking up your account now" and use lookup_customer tool
    
    AVAILABLE SCENARIOS after verification:
    - ACCOUNT BALANCE CHECK: Provide current balance, next payment amount/date, ask about payment confirmation
    - ARREARS MANAGEMENT: Present 3 options (full payment, split arrears, increase payments)
    - PAYMENT DEFERRALS: Handle one-time or ongoing payment changes, 2 business days notice required
    - HARDSHIP ASSISTANCE: Collect hardship reason, transfer to specialist team
    - BANKING UPDATES: Collect new bank details, send email confirmation
    - PORTAL ISSUES: Handle login problems while addressing main inquiry
    
    CLOSING CHECKLIST:
    1. Summarize actions taken
    2. Confirm follow-up actions 
    3. Ask "Is there anything else I can help you with today?"
    4. Thank customer and end call
    
    RULES: One question at a time, use lookup_customer after collecting all verification information.
    """
    customer_input: str = dspy.InputField(desc="What the customer just said")
    history: dspy.History = dspy.InputField(desc="Conversation history")
    
    response: str = dspy.OutputField(desc="Assistant response following Sky Credit protocols")

