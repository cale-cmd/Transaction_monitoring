
from rules.base_rule import BaseRule
from typing import Optional, Dict
from datetime import datetime, timedelta
import config


class RapidSuccessionRule(BaseRule):

    def __init__(self):
        super().__init__("RAPID_SUCCESSION")
        self.time_window = config.RAPID_SUCCESSION_WINDOW 
    
    def evaluate(self, transaction, db) -> Optional[Dict]:

        user_id = transaction.user_id
        current_time = transaction.get_timestamp_obj()
        

        window_start = (current_time - timedelta(seconds=self.time_window)).isoformat()
        recent_transactions = db.get_user_transactions_in_window(
            user_id,
            window_start,
            current_time.isoformat()
        )
        
   
        if len(recent_transactions) >= 2:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'{len(recent_transactions) + 1} transactions within {self.time_window} seconds'
            }
        elif len(recent_transactions) == 1:

            prev_txn_time = datetime.fromisoformat(recent_transactions[0]['timestamp'])
            time_diff = (current_time - prev_txn_time).total_seconds()
            
            if time_diff < 30: 
                return {
                    'triggered': True,
                    'rule_name': self.name,
                    'severity': 'MEDIUM',
                    'details': f'2 transactions within {time_diff:.0f} seconds'
                }
        
        return None