
DATABASE_PATH = "transaction_monitor.db"


AMOUNT_THRESHOLD_MEDIUM = 200000 
AMOUNT_THRESHOLD_HIGH = 500000  


VELOCITY_MAX_PER_HOUR = 5
VELOCITY_MAX_PER_DAY = 10
VELOCITY_MAX_PER_MINUTE = 3


DAILY_LIMIT_MEDIUM = 500000  
DAILY_LIMIT_HIGH = 1000000   


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


RAPID_SUCCESSION_WINDOW = 60
VELOCITY_HOUR_WINDOW = 3600
VELOCITY_DAY_WINDOW = 86400


API_HOST = "0.0.0.0"
API_PORT = 5000
DEBUG_MODE = True

LOG_LEVEL = "INFO"
LOG_FILE = "logs/app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"