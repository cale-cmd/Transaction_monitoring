"""
Amount Threshold Rule

Flags transactions that exceed certain amount limits.
"""

from rules.base_rule import BaseRule
from typing import Optional, Dict
import config


class AmountThresholdRule(BaseRule):
    """
    Checks if transaction amount exceeds thresholds
    
    Logic:
    - Amount > HIGH threshold → HIGH severity alert
    - Amount > MEDIUM threshold → MEDIUM severity alert
    - Otherwise → No alert
    """
    
    def __init__(self):
        super().__init__("AMOUNT_THRESHOLD")
        self.medium_threshold = config.AMOUNT_THRESHOLD_MEDIUM
        self.high_threshold = config.AMOUNT_THRESHOLD_HIGH
    
    def evaluate(self, transaction, db) -> Optional[Dict]:
        """
        Check if transaction amount is too high
        
        Args:
            transaction: Transaction object
            db: Database object (not used by this rule)
        
        Returns:
            Alert details if triggered, None otherwise
        """
        amount = transaction.amount
        
        # Check HIGH threshold first (more severe)
        if amount > self.high_threshold:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'Amount ₹{amount:,.0f} exceeds high threshold of ₹{self.high_threshold:,.0f}'
            }
        
        # Check MEDIUM threshold
        elif amount > self.medium_threshold:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'MEDIUM',
                'details': f'Amount ₹{amount:,.0f} exceeds medium threshold of ₹{self.medium_threshold:,.0f}'
            }
        
        # No threshold exceeded
        return None