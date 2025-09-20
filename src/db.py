"""
Database functionality for Sky Credit Voice Assistant
Contains customer database and lookup functions using Pydantic models.
"""

from typing import Dict, Optional
from pydantic import BaseModel

class Customer(BaseModel):
    """Customer account information model"""
    firstName: str
    lastName: str
    emailAddress: str
    mobileNumber: str
    clientReferenceNumber: str
    accountBalance: float
    arrearsBalance: float
    minimumAmountDue: float
    nextPaymentDate: str
    accountStatus: str
    daysPastDue: int

# Customer database using Pydantic models
CUSTOMER_DATABASE = {
    "XT59591": Customer(firstName="Paul", lastName="Walshe", emailAddress="paul.w@fintech-services.com.au", mobileNumber="+61402017491", clientReferenceNumber="XT59591", accountBalance=1491.06, arrearsBalance=521.87, minimumAmountDue=149.11, nextPaymentDate="2025-09-17", accountStatus="Arrears", daysPastDue=12),
    "PO18973": Customer(firstName="Greg", lastName="Haynes", emailAddress="greg.h@fintech-services.com.au", mobileNumber="+61403893026", clientReferenceNumber="PO18973", accountBalance=1262, arrearsBalance=441.7, minimumAmountDue=126.2, nextPaymentDate="2025-09-09", accountStatus="Arrears", daysPastDue=45),
    "HA79343": Customer(firstName="Alice", lastName="Tapu", emailAddress="alice.t@fairgofinance.com.au", mobileNumber="+61498043748", clientReferenceNumber="HA79343", accountBalance=104.21, arrearsBalance=36.47, minimumAmountDue=10.42, nextPaymentDate="2025-09-21", accountStatus="Arrears", daysPastDue=7),
    "SD89885": Customer(firstName="Wendy", lastName="Proudfoot", emailAddress="wendy.p@fairgofinance.com.au", mobileNumber="+61402643302", clientReferenceNumber="SD89885", accountBalance=320.23, arrearsBalance=112.08, minimumAmountDue=32.02, nextPaymentDate="2025-09-03", accountStatus="Arrears", daysPastDue=13),
    "KE75413": Customer(firstName="Madisson", lastName="McCrystal", emailAddress="madisson.m@fairgofinance.com.au", mobileNumber="+61487914945", clientReferenceNumber="KE75413", accountBalance=1773.46, arrearsBalance=620.71, minimumAmountDue=177.35, nextPaymentDate="2025-09-15", accountStatus="Arrears", daysPastDue=43),
    "ZZ99466": Customer(firstName="Rachel", lastName="Clark", emailAddress="mayjason@gmail.com", mobileNumber="+6140389301", clientReferenceNumber="ZZ99466", accountBalance=1587.08, arrearsBalance=555.48, minimumAmountDue=158.71, nextPaymentDate="2025-09-23", accountStatus="Arrears", daysPastDue=15),
    "KQ59118": Customer(firstName="Jennifer", lastName="Reeves", emailAddress="watkinsnicole@gonzalez.com", mobileNumber="+6140389302", clientReferenceNumber="KQ59118", accountBalance=150.59, arrearsBalance=52.71, minimumAmountDue=15.06, nextPaymentDate="2025-09-25", accountStatus="Arrears", daysPastDue=54),
    "UD62179": Customer(firstName="Marcus", lastName="Moore", emailAddress="qschultz@yahoo.com", mobileNumber="+6140389303", clientReferenceNumber="UD62179", accountBalance=89.63, arrearsBalance=31.37, minimumAmountDue=8.96, nextPaymentDate="2025-09-21", accountStatus="Arrears", daysPastDue=23),
    "IF42330": Customer(firstName="Karen", lastName="Cortez", emailAddress="adam18@fox.biz", mobileNumber="+6140389304", clientReferenceNumber="IF42330", accountBalance=547.53, arrearsBalance=191.64, minimumAmountDue=54.75, nextPaymentDate="2025-09-18", accountStatus="Arrears", daysPastDue=12),
    "LF36852": Customer(firstName="Jane", lastName="Clark", emailAddress="vliu@gmail.com", mobileNumber="+6140389305", clientReferenceNumber="LF36852", accountBalance=1055.38, arrearsBalance=369.38, minimumAmountDue=105.54, nextPaymentDate="2025-09-28", accountStatus="Arrears", daysPastDue=124)
}

# Mobile number to reference mapping for quick lookup
MOBILE_TO_REFERENCE = {
    "+61402017491": "XT59591",
    "+61403893026": "PO18973", 
    "+61498043748": "HA79343",
    "+61402643302": "SD89885",
    "+61487914945": "KE75413",
    "+6140389301": "ZZ99466",
    "+6140389302": "KQ59118",
    "+6140389303": "UD62179",
    "+6140389304": "IF42330",
    "+6140389305": "LF36852"
}

def lookup_customer(reference_or_mobile: str, first_name: str, last_name: str) -> Optional[Customer]:
    """Look up customer in the database using Pydantic models"""
    # Clean input
    reference_or_mobile = reference_or_mobile.strip().upper()
    first_name = first_name.strip().lower()
    last_name = last_name.strip().lower()
    
    # First try direct reference lookup (most efficient)
    if reference_or_mobile in CUSTOMER_DATABASE:
        customer = CUSTOMER_DATABASE[reference_or_mobile]
        if (customer.firstName.lower() == first_name and 
            customer.lastName.lower() == last_name):
            return customer
    
    # Try mobile number lookup
    cleaned_mobile = reference_or_mobile.replace("+", "").replace(" ", "").replace("-", "")
    for mobile, ref in MOBILE_TO_REFERENCE.items():
        if mobile.replace("+", "").replace(" ", "") == cleaned_mobile:
            customer = CUSTOMER_DATABASE[ref]
            if (customer.firstName.lower() == first_name and 
                customer.lastName.lower() == last_name):
                return customer
    
    return None