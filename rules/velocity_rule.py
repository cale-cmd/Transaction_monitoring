"""
Velocity Rule

Flags users making too many transactions in a short time period.
Detects potential fraud where stolen cards are used rapidly.
"""

from rules.base_rule import BaseRule
from typing import Optional, Dict
from datetime import datetime, timedelta
import config


class VelocityRule(BaseRule):
    """
    Checks transaction frequency for a user
    
    Logic:
    - Count transactions by user in different time windows
    - Alert if count exceeds threshold for any window
    """
    
    def __init__(self):
        super().__init__("VELOCITY")
        self.max_per_hour = config.VELOCITY_MAX_PER_HOUR
        self.max_per_day = config.VELOCITY_MAX_PER_DAY
        self.max_per_minute = config.VELOCITY_MAX_PER_MINUTE
    
    def evaluate(self, transaction, db) -> Optional[Dict]:
        """
        Check if user is transacting too frequently
        
        Args:
            transaction: Transaction object
            db: Database object to query transaction history
        
        Returns:
            Alert details if triggered, None otherwise
        """
        user_id = transaction.user_id
        current_time = transaction.get_timestamp_obj()
        
        # Check last minute (CRITICAL - very fast transactions)
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
        
        # Check last hour (HIGH priority)
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
        
        # Check last 24 hours (MEDIUM priority)
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
        
        # No velocity threshold exceeded
        return None