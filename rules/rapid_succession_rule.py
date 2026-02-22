"""
Rapid Succession Rule

Flags multiple transactions within seconds of each other.
Detects automated bot attacks or someone testing a stolen card.
"""

from rules.base_rule import BaseRule
from typing import Optional, Dict
from datetime import datetime, timedelta
import config


class RapidSuccessionRule(BaseRule):
    """
    Checks if transactions are happening too quickly (within 60 seconds)
    
    Logic:
    - Count transactions by user in last 60 seconds
    - If 2+ transactions that fast, it's suspicious
    """
    
    def __init__(self):
        super().__init__("RAPID_SUCCESSION")
        self.time_window = config.RAPID_SUCCESSION_WINDOW  # 60 seconds
    
    def evaluate(self, transaction, db) -> Optional[Dict]:
        """
        Check if user made recent transactions very quickly
        
        Args:
            transaction: Transaction object
            db: Database object to query transaction history
        
        Returns:
            Alert details if triggered, None otherwise
        """
        user_id = transaction.user_id
        current_time = transaction.get_timestamp_obj()
        
        # Get transactions from last 60 seconds
        window_start = (current_time - timedelta(seconds=self.time_window)).isoformat()
        recent_transactions = db.get_user_transactions_in_window(
            user_id,
            window_start,
            current_time.isoformat()
        )
        
        # If there are already 2+ transactions in this window, flag it
        if len(recent_transactions) >= 2:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'{len(recent_transactions) + 1} transactions within {self.time_window} seconds'
            }
        elif len(recent_transactions) == 1:
            # Calculate time difference
            prev_txn_time = datetime.fromisoformat(recent_transactions[0]['timestamp'])
            time_diff = (current_time - prev_txn_time).total_seconds()
            
            if time_diff < 30:  # Less than 30 seconds
                return {
                    'triggered': True,
                    'rule_name': self.name,
                    'severity': 'MEDIUM',
                    'details': f'2 transactions within {time_diff:.0f} seconds'
                }
        
        return None