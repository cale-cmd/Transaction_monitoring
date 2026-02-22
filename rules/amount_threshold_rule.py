
from rules.base_rule import BaseRule
from typing import Optional, Dict
import config


class AmountThresholdRule(BaseRule):
    
    def __init__(self):
        super().__init__("AMOUNT_THRESHOLD")
        self.medium_threshold = config.AMOUNT_THRESHOLD_MEDIUM
        self.high_threshold = config.AMOUNT_THRESHOLD_HIGH
    
    def evaluate(self, transaction, db) -> Optional[Dict]:

        amount = transaction.amount
        

        if amount > self.high_threshold:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'Amount ₹{amount:,.0f} exceeds high threshold of ₹{self.high_threshold:,.0f}'
            }
        

        elif amount > self.medium_threshold:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'MEDIUM',
                'details': f'Amount ₹{amount:,.0f} exceeds medium threshold of ₹{self.medium_threshold:,.0f}'
            }
        

        return None