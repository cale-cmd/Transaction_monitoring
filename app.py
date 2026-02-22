
from flask import Flask
from api.routes import api, init_routes
from database.db import Database
from services.rule_engine import RuleEngine
from services.alert_manager import AlertManager
from services.transaction_service import TransactionService
from utils.logger import setup_logger, logger
import config
import os


def create_app():


    app = Flask(__name__)
    

    logger.info("=" * 50)
    logger.info("Starting Transaction Monitoring API")
    logger.info("=" * 50)
    

    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        logger.info(f"Created logs directory: {log_dir}")
    

    logger.info(f"Initializing database: {config.DATABASE_PATH}")
    db = Database(config.DATABASE_PATH)
    logger.info("Database initialized successfully")
    

    logger.info("Initializing services...")
    rule_engine = RuleEngine()
    logger.info(f"Rule engine initialized with {len(rule_engine.get_active_rules())} active rules")
    
    alert_manager = AlertManager(db)
    logger.info("Alert manager initialized")
    
    transaction_service = TransactionService(db, rule_engine, alert_manager)
    logger.info("Transaction service initialized")
    

    init_routes(transaction_service, alert_manager)
    logger.info("API routes initialized")
    

    app.register_blueprint(api)
    logger.info("API blueprint registered")
    
    logger.info("=" * 50)
    logger.info("Application initialization complete")
    logger.info(f"API will listen on {config.API_HOST}:{config.API_PORT}")
    logger.info("=" * 50)
    
    return app


if __name__ == '__main__':

    app = create_app()
    
    logger.info("Starting Flask server...")
    
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.DEBUG_MODE
    )