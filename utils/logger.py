"""
Logging configuration

Sets up structured logging for the application.
"""

import logging
import os
from datetime import datetime
import config


def setup_logger(name: str = 'transaction_monitor') -> logging.Logger:
    """
    Configure and return a logger
    
    Args:
        name: Logger name
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Prevent duplicate logs
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # File handler (writes to file)
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler (writes to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create global logger instance
logger = setup_logger()


def log_transaction(transaction):
    """
    Log transaction details
    
    Args:
        transaction: Transaction object
    """
    logger.info(
        f"Transaction processed: {transaction.transaction_id} | "
        f"User: {transaction.user_id} | "
        f"Amount: ₹{transaction.amount:,.0f} | "
        f"Merchant: {transaction.merchant_category}"
    )


def log_alert(alert):
    """
    Log alert generation
    
    Args:
        alert: Alert object
    """
    logger.warning(
        f"ALERT GENERATED: {alert.alert_id} | "
        f"Rule: {alert.rule_name} | "
        f"Severity: {alert.severity} | "
        f"Transaction: {alert.transaction_id} | "
        f"Details: {alert.details}"
    )


def log_api_request(method: str, endpoint: str, status_code: int, duration: float = None):
    """
    Log API requests
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        status_code: HTTP status code
        duration: Request duration in seconds (optional)
    """
    duration_str = f" | Duration: {duration:.3f}s" if duration else ""
    logger.info(
        f"API {method} {endpoint} | Status: {status_code}{duration_str}"
    )


def log_error(error_message: str, exception: Exception = None):
    """
    Log errors with optional exception details
    
    Args:
        error_message: Error description
        exception: Exception object (optional)
    """
    if exception:
        logger.error(f"{error_message} | Exception: {str(exception)}", exc_info=True)
    else:
        logger.error(error_message)