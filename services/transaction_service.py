
from typing import Dict, List, Optional
from models.transaction import Transaction
from datetime import datetime
import uuid


class TransactionService:

    def __init__(self, db, rule_engine, alert_manager):

        self.db = db
        self.rule_engine = rule_engine
        self.alert_manager = alert_manager
    
    def process_transaction(self, transaction_data: dict) -> Dict:

        transaction = Transaction.from_dict(transaction_data)
        
  
        self.db.insert_transaction(transaction)
        
  
        rule_results = self.rule_engine.evaluate_transaction(transaction, self.db)
        
    
        alerts = []
        for rule_result in rule_results:
            alert = self.alert_manager.create_alert(transaction, rule_result)
            alerts.append(alert)
        
     
        status = 'FLAGGED' if len(alerts) > 0 else 'APPROVED'
        
   
        return {
            'transaction_id': transaction.transaction_id,
            'status': status,
            'alerts': [alert.to_dict() for alert in alerts],
            'alert_count': len(alerts)
        }
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict]:

        return self.db.get_transaction(transaction_id)
    
    def get_transactions(self, user_id: str = None, 
                        start_date: str = None, 
                        end_date: str = None) -> List[Dict]:

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