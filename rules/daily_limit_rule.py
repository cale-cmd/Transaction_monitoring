
from rules.base_rule import BaseRule
from typing import Optional, Dict
from datetime import datetime, timedelta
import config


class DailyLimitRule(BaseRule):

    def __init__(self):
        super().__init__("DAILY_LIMIT")
        self.medium_limit = config.DAILY_LIMIT_MEDIUM
        self.high_limit = config.DAILY_LIMIT_HIGH
    
    def evaluate(self, transaction, db) -> Optional[Dict]:

        user_id = transaction.user_id
        current_time = transaction.get_timestamp_obj()
        

        one_day_ago = (current_time - timedelta(days=1)).isoformat()
        recent_transactions = db.get_user_transactions_in_window(
            user_id,
            one_day_ago,
            current_time.isoformat()
        )
        

        total_amount = sum(txn['amount'] for txn in recent_transactions)
        

        if total_amount > self.high_limit:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'Total spending ₹{total_amount:,.0f} in 24h exceeds high limit of ₹{self.high_limit:,.0f} ({len(recent_transactions)} transactions)'
            }
      
        elif total_amount > self.medium_limit:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'MEDIUM',
                'details': f'Total spending ₹{total_amount:,.0f} in 24h exceeds medium limit of ₹{self.medium_limit:,.0f} ({len(recent_transactions)} transactions)'
            }
        
        return None