
from rules.base_rule import BaseRule
from typing import Optional, Dict
from datetime import datetime, timedelta
import config


class VelocityRule(BaseRule):

    
    def __init__(self):
        super().__init__("VELOCITY")
        self.max_per_hour = config.VELOCITY_MAX_PER_HOUR
        self.max_per_day = config.VELOCITY_MAX_PER_DAY
        self.max_per_minute = config.VELOCITY_MAX_PER_MINUTE
    
    def evaluate(self, transaction, db) -> Optional[Dict]:

        user_id = transaction.user_id
        current_time = transaction.get_timestamp_obj()
        
 
        one_minute_ago = (current_time - timedelta(seconds=60)).isoformat()
        recent_minute = db.get_user_transactions_in_window(
            user_id, 
            one_minute_ago,
            current_time.isoformat()
        )
        
        if len(recent_minute) >= self.max_per_minute:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'CRITICAL',
                'details': f'User made {len(recent_minute)} transactions in last minute (limit: {self.max_per_minute})'
            }
        

        one_hour_ago = (current_time - timedelta(hours=1)).isoformat()
        recent_hour = db.get_user_transactions_in_window(
            user_id, 
            one_hour_ago,
            current_time.isoformat()
        )
        
        if len(recent_hour) >= self.max_per_hour:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'User made {len(recent_hour)} transactions in last hour (limit: {self.max_per_hour})'
            }
        

        one_day_ago = (current_time - timedelta(days=1)).isoformat()
        recent_day = db.get_user_transactions_in_window(
            user_id, 
            one_day_ago,
            current_time.isoformat()
        )
        
        if len(recent_day) >= self.max_per_day:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'MEDIUM',
                'details': f'User made {len(recent_day)} transactions in last 24 hours (limit: {self.max_per_day})'
            }
        

        return None