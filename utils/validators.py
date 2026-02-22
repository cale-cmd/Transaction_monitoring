"""
Input validation functions

Validates incoming data to ensure it's safe and correct.
"""

from typing import Tuple, Dict
from datetime import datetime


def validate_transaction_data(data: dict) -> Tuple[bool, str]:
    """
    Validate incoming transaction data
    
    Args:
        data: Dictionary with transaction data
    
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    # Check required fields
    required_fields = [
        'user_id', 'amount', 'merchant_id', 
        'merchant_category', 'payment_method'
    ]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate user_id format
    is_valid, error = validate_user_id(data['user_id'])
    if not is_valid:
        return False, error
    
    # Validate amount
    is_valid, error = validate_amount(data['amount'])
    if not is_valid:
        return False, error
    
    # Validate merchant_id
    if not data['merchant_id'] or len(data['merchant_id']) < 3:
        return False, "Invalid merchant_id"
    
    # Validate merchant_category
    if not data['merchant_category'] or len(data['merchant_category']) < 3:
        return False, "Invalid merchant_category"
    
    # Validate payment_method
    valid_payment_methods = [
        'credit_card', 'debit_card', 'upi', 
        'net_banking', 'wallet', 'cash'
    ]
    if data['payment_method'] not in valid_payment_methods:
        return False, f"Invalid payment_method. Must be one of: {', '.join(valid_payment_methods)}"
    
    # Validate timestamp if provided
    if 'timestamp' in data:
        is_valid, error = validate_timestamp(data['timestamp'])
        if not is_valid:
            return False, error
    
    # All validations passed
    return True, None


def validate_amount(amount) -> Tuple[bool, str]:
    """
    Validate amount field
    
    Args:
        amount: Amount value
    
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    try:
        amount_float = float(amount)
    except (ValueError, TypeError):
        return False, "Amount must be a valid number"
    
    if amount_float <= 0:
        return False, "Amount must be greater than 0"
    
    if amount_float > 100000000:  # 10 crore limit
        return False, "Amount exceeds maximum limit of ₹10,00,00,000"
    
    return True, None


def validate_user_id(user_id: str) -> Tuple[bool, str]:
    """
    Validate user_id format
    
    Args:
        user_id: User ID string
    
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    if not user_id or not isinstance(user_id, str):
        return False, "user_id must be a non-empty string"
    
    if len(user_id) < 3:
        return False, "user_id must be at least 3 characters"
    
    if len(user_id) > 100:
        return False, "user_id must be less than 100 characters"
    
    return True, None


def validate_timestamp(timestamp: str) -> Tuple[bool, str]:
    """
    Validate timestamp format
    
    Args:
        timestamp: Timestamp string
    
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    try:
        datetime.fromisoformat(timestamp)
        return True, None
    except (ValueError, TypeError):
        return False, "timestamp must be in ISO 8601 format (e.g., '2026-01-26T14:30:00')"


def validate_alert_resolution(data: dict) -> Tuple[bool, str]:
    """
    Validate alert resolution data
    
    Args:
        data: Dictionary with resolution data
    
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    # Check required fields
    if 'resolution' not in data:
        return False, "Missing required field: resolution"
    
    if 'reviewed_by' not in data:
        return False, "Missing required field: reviewed_by"
    
    # Validate resolution status
    valid_resolutions = ['APPROVED', 'REJECTED', 'FALSE_POSITIVE']
    if data['resolution'] not in valid_resolutions:
        return False, f"Invalid resolution. Must be one of: {', '.join(valid_resolutions)}"
    
    return True, None