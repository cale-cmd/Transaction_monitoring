"""
Transaction Service

Business logic for handling transactions.
This orchestrates the entire transaction monitoring workflow.
"""

from typing import Dict, List, Optional
from models.transaction import Transaction
from datetime import datetime
import uuid


class TransactionService:
    """
    Handles transaction processing and storage
    
    This is the MAIN ORCHESTRATOR that coordinates:
    - Transaction creation and storage
    - Rule evaluation
    - Alert generation
    - Reporting
    """
    
    def __init__(self, db, rule_engine, alert_manager):
        """
        Initialize transaction service
        
        Args:
            db: Database object
            rule_engine: RuleEngine instance
            alert_manager: AlertManager instance
        """
        self.db = db
        self.rule_engine = rule_engine
        self.alert_manager = alert_manager
    
    def process_transaction(self, transaction_data: dict) -> Dict:
        """
        Process a new transaction
        
        This is the MAIN WORKFLOW:
        1. Create Transaction object from input data
        2. Save transaction to database
        3. Run all rules against transaction
        4. Create alerts for any triggered rules
        5. Return result with status and alerts
        
        Args:
            transaction_data: Dictionary with transaction info
        
        Returns:
            Dictionary with processing result:
            {
                'transaction_id': 'TXN_...',
                'status': 'APPROVED' or 'FLAGGED',
                'alerts': [list of alert objects],
                'alert_count': number of alerts
            }
        """
        # Step 1: Create Transaction object
        transaction = Transaction.from_dict(transaction_data)
        
        # Step 2: Save to database
        self.db.insert_transaction(transaction)
        
        # Step 3: Run rules
        rule_results = self.rule_engine.evaluate_transaction(transaction, self.db)
        
        # Step 4: Create alerts for triggered rules
        alerts = []
        for rule_result in rule_results:
            alert = self.alert_manager.create_alert(transaction, rule_result)
            alerts.append(alert)
        
        # Step 5: Determine status
        status = 'FLAGGED' if len(alerts) > 0 else 'APPROVED'
        
        # Return result
        return {
            'transaction_id': transaction.transaction_id,
            'status': status,
            'alerts': [alert.to_dict() for alert in alerts],
            'alert_count': len(alerts)
        }
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """
        Retrieve a transaction by ID
        
        Args:
            transaction_id: Transaction ID to find
        
        Returns:
            Transaction dictionary or None
        """
        return self.db.get_transaction(transaction_id)
    
    def get_transactions(self, user_id: str = None, 
                        start_date: str = None, 
                        end_date: str = None) -> List[Dict]:
        """
        Retrieve transactions with optional filters
        
        Args:
            user_id: Filter by user ID (optional)
            start_date: Start of date range (optional)
            end_date: End of date range (optional)
        
        Returns:
            List of transaction dictionaries
        """
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp DESC"
        
        return self.db.execute_query(query, tuple(params) if params else None)
    
    def get_user_statistics(self, user_id: str) -> Dict:
        """
        Get statistics for a specific user
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with user statistics
        """
        transactions = self.db.execute_query(
            "SELECT * FROM transactions WHERE user_id = ?",
            (user_id,)
        )
        
        if not transactions:
            return {
                'user_id': user_id,
                'total_transactions': 0,
                'total_amount': 0,
                'average_amount': 0
            }
        
        total_amount = sum(txn['amount'] for txn in transactions)
        
        return {
            'user_id': user_id,
            'total_transactions': len(transactions),
            'total_amount': total_amount,
            'average_amount': total_amount / len(transactions),
            'first_transaction': transactions[-1]['timestamp'],
            'last_transaction': transactions[0]['timestamp']
        }