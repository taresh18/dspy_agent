"""
Database functionality for Sky Credit Voice Assistant
Contains customer database and lookup functions.
"""

from typing import Dict, Optional

# Customer database as provided in the prompt
CUSTOMER_DATABASE = [
    {"firstName": "Paul", "lastName": "Walshe", "emailAddress": "paul.w@fintech-services.com.au", "mobileNumber": "+61402017491", "clientReferenceNumber": "XT59591", "accountBalance": 1491.06, "arrearsBalance": 521.87, "minimumAmountDue": 149.11, "nextPaymentDate": "2025-09-17", "accountStatus": "Arrears", "daysPastDue": 12},
    {"firstName": "Greg", "lastName": "Haynes", "emailAddress": "greg.h@fintech-services.com.au", "mobileNumber": "+61403893026", "clientReferenceNumber": "PO18973", "accountBalance": 1262, "arrearsBalance": 441.7, "minimumAmountDue": 126.2, "nextPaymentDate": "2025-09-09", "accountStatus": "Arrears", "daysPastDue": 45},
    {"firstName": "Alice", "lastName": "Tapu", "emailAddress": "alice.t@fairgofinance.com.au", "mobileNumber": "+61498043748", "clientReferenceNumber": "HA79343", "accountBalance": 104.21, "arrearsBalance": 36.47, "minimumAmountDue": 10.42, "nextPaymentDate": "2025-09-21", "accountStatus": "Arrears", "daysPastDue": 7},
    {"firstName": "Wendy", "lastName": "Proudfoot", "emailAddress": "wendy.p@fairgofinance.com.au", "mobileNumber": "+61402643302", "clientReferenceNumber": "SD89885", "accountBalance": 320.23, "arrearsBalance": 112.08, "minimumAmountDue": 32.02, "nextPaymentDate": "2025-09-03", "accountStatus": "Arrears", "daysPastDue": 13},
    {"firstName": "Madisson", "lastName": "McCrystal", "emailAddress": "madisson.m@fairgofinance.com.au", "mobileNumber": "+61487914945", "clientReferenceNumber": "KE75413", "accountBalance": 1773.46, "arrearsBalance": 620.71, "minimumAmountDue": 177.35, "nextPaymentDate": "2025-09-15", "accountStatus": "Arrears", "daysPastDue": 43},
    {"firstName": "Rachel", "lastName": "Clark", "emailAddress": "mayjason@gmail.com", "mobileNumber": "+6140389301", "clientReferenceNumber": "ZZ99466", "accountBalance": 1587.08, "arrearsBalance": 555.48, "minimumAmountDue": 158.71, "nextPaymentDate": "2025-09-23", "accountStatus": "Arrears", "daysPastDue": 15},
    {"firstName": "Jennifer", "lastName": "Reeves", "emailAddress": "watkinsnicole@gonzalez.com", "mobileNumber": "+6140389302", "clientReferenceNumber": "KQ59118", "accountBalance": 150.59, "arrearsBalance": 52.71, "minimumAmountDue": 15.06, "nextPaymentDate": "2025-09-25", "accountStatus": "Arrears", "daysPastDue": 54},
    {"firstName": "Marcus", "lastName": "Moore", "emailAddress": "qschultz@yahoo.com", "mobileNumber": "+6140389303", "clientReferenceNumber": "UD62179", "accountBalance": 89.63, "arrearsBalance": 31.37, "minimumAmountDue": 8.96, "nextPaymentDate": "2025-09-21", "accountStatus": "Arrears", "daysPastDue": 23},
    {"firstName": "Karen", "lastName": "Cortez", "emailAddress": "adam18@fox.biz", "mobileNumber": "+6140389304", "clientReferenceNumber": "IF42330", "accountBalance": 547.53, "arrearsBalance": 191.64, "minimumAmountDue": 54.75, "nextPaymentDate": "2025-09-18", "accountStatus": "Arrears", "daysPastDue": 12},
    {"firstName": "Jane", "lastName": "Clark", "emailAddress": "vliu@gmail.com", "mobileNumber": "+6140389305", "clientReferenceNumber": "LF36852", "accountBalance": 1055.38, "arrearsBalance": 369.38, "minimumAmountDue": 105.54, "nextPaymentDate": "2025-09-28", "accountStatus": "Arrears", "daysPastDue": 124}
]

def lookup_customer(reference_or_mobile: str, first_name: str, last_name: str) -> Optional[Dict]:
    """Look up customer in the database"""
    for customer in CUSTOMER_DATABASE:
        customer_ref = customer.get("clientReferenceNumber", "")
        customer_mobile = customer.get("mobileNumber", "")
        customer_fname = customer.get("firstName", "")
        customer_lname = customer.get("lastName", "")
        
        # Check by reference number or mobile number
        if (customer_ref.lower() == reference_or_mobile.lower() or
            customer_mobile.replace("+", "").replace(" ", "") == reference_or_mobile.replace("+", "").replace(" ", "")):
            # Verify name match
            if (customer_fname.lower() == first_name.lower() and
                customer_lname.lower() == last_name.lower()):
                return customer
    
    return None

def get_customer_by_reference(reference_number: str) -> Optional[Dict]:
    """Get customer by reference number only"""
    for customer in CUSTOMER_DATABASE:
        if customer.get("clientReferenceNumber", "").lower() == reference_number.lower():
            return customer
    return None

def get_customer_by_mobile(mobile_number: str) -> Optional[Dict]:
    """Get customer by mobile number only"""
    cleaned_mobile = mobile_number.replace("+", "").replace(" ", "").replace("-", "")
    for customer in CUSTOMER_DATABASE:
        customer_mobile = customer.get("mobileNumber", "").replace("+", "").replace(" ", "").replace("-", "")
        if customer_mobile == cleaned_mobile:
            return customer
    return None

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_date(date_str: str) -> str:
    """Format date string for voice output"""
    # You can add date formatting logic here if needed
    return date_str

