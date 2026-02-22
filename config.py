"""
Configuration settings for the transaction monitoring system
"""

# Database
DATABASE_PATH = "transaction_monitor.db"

# Amount threshold settings
AMOUNT_THRESHOLD_MEDIUM = 200000  # ₹2 lakhs
AMOUNT_THRESHOLD_HIGH = 500000    # ₹5 lakhs

# Velocity settings
VELOCITY_MAX_PER_HOUR = 5
VELOCITY_MAX_PER_DAY = 10
VELOCITY_MAX_PER_MINUTE = 3

# Daily limit settings
DAILY_LIMIT_MEDIUM = 500000   # ₹5 lakhs
DAILY_LIMIT_HIGH = 1000000    # ₹10 lakhs

# High-risk merchant categories
HIGH_RISK_MERCHANTS = [
    "crypto_exchange",
    "gambling",
    "betting",
    "wire_transfer",
    "cash_advance",
    "money_transfer"
]

MEDIUM_RISK_MERCHANTS = [
    "jewelry",
    "precious_metals",
    "luxury_goods"
]

# Time windows (in seconds)
RAPID_SUCCESSION_WINDOW = 60
VELOCITY_HOUR_WINDOW = 3600
VELOCITY_DAY_WINDOW = 86400

# API settings
API_HOST = "0.0.0.0"
API_PORT = 5000
DEBUG_MODE = True

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"