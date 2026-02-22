
import logging
import os
from datetime import datetime
import config


def setup_logger(name: str = 'transaction_monitor') -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    

    if logger.handlers:
        return logger
    

    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    

    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    

    formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger



logger = setup_logger()


def log_transaction(transaction):

    logger.info(
        f"Transaction processed: {transaction.transaction_id} | "
        f"User: {transaction.user_id} | "
        f"Amount: ₹{transaction.amount:,.0f} | "
        f"Merchant: {transaction.merchant_category}"
    )


def log_alert(alert):

    logger.warning(
        f"ALERT GENERATED: {alert.alert_id} | "
        f"Rule: {alert.rule_name} | "
        f"Severity: {alert.severity} | "
        f"Transaction: {alert.transaction_id} | "
        f"Details: {alert.details}"
    )


def log_api_request(method: str, endpoint: str, status_code: int, duration: float = None):

    duration_str = f" | Duration: {duration:.3f}s" if duration else ""
    logger.info(
        f"API {method} {endpoint} | Status: {status_code}{duration_str}"
    )


def log_error(error_message: str, exception: Exception = None):

    if exception:
        logger.error(f"{error_message} | Exception: {str(exception)}", exc_info=True)
    else:
        logger.error(error_message)