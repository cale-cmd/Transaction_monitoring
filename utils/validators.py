
from typing import Tuple, Dict
from datetime import datetime


def validate_transaction_data(data: dict) -> Tuple[bool, str]:

    required_fields = [
        'user_id', 'amount', 'merchant_id', 
        'merchant_category', 'payment_method'
    ]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    

    is_valid, error = validate_user_id(data['user_id'])
    if not is_valid:
        return False, error
    

    is_valid, error = validate_amount(data['amount'])
    if not is_valid:
        return False, error
    

    if not data['merchant_id'] or len(data['merchant_id']) < 3:
        return False, "Invalid merchant_id"
    

    if not data['merchant_category'] or len(data['merchant_category']) < 3:
        return False, "Invalid merchant_category"
    

    valid_payment_methods = [
        'credit_card', 'debit_card', 'upi', 
        'net_banking', 'wallet', 'cash'
    ]
    if data['payment_method'] not in valid_payment_methods:
        return False, f"Invalid payment_method. Must be one of: {', '.join(valid_payment_methods)}"
    

    if 'timestamp' in data:
        is_valid, error = validate_timestamp(data['timestamp'])
        if not is_valid:
            return False, error
    

    return True, None


def validate_amount(amount) -> Tuple[bool, str]:

    try:
        amount_float = float(amount)
    except (ValueError, TypeError):
        return False, "Amount must be a valid number"
    
    if amount_float <= 0:
        return False, "Amount must be greater than 0"
    
    if amount_float > 100000000:
        return False, "Amount exceeds maximum limit of ₹10,00,00,000"
    
    return True, None


def validate_user_id(user_id: str) -> Tuple[bool, str]:

    if not user_id or not isinstance(user_id, str):
        return False, "user_id must be a non-empty string"
    
    if len(user_id) < 3:
        return False, "user_id must be at least 3 characters"
    
    if len(user_id) > 100:
        return False, "user_id must be less than 100 characters"
    
    return True, None


def validate_timestamp(timestamp: str) -> Tuple[bool, str]:

    try:
        datetime.fromisoformat(timestamp)
        return True, None
    except (ValueError, TypeError):
        return False, "timestamp must be in ISO 8601 format (e.g., '2026-01-26T14:30:00')"


def validate_alert_resolution(data: dict) -> Tuple[bool, str]:

    if 'resolution' not in data:
        return False, "Missing required field: resolution"
    
    if 'reviewed_by' not in data:
        return False, "Missing required field: reviewed_by"
    

    valid_resolutions = ['APPROVED', 'REJECTED', 'FALSE_POSITIVE']
    if data['resolution'] not in valid_resolutions:
        return False, f"Invalid resolution. Must be one of: {', '.join(valid_resolutions)}"
    
    return True, None