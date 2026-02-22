
from rules.base_rule import BaseRule
from typing import Optional, Dict
import config


class HighRiskMerchantRule(BaseRule):

    def __init__(self):
        super().__init__("HIGH_RISK_MERCHANT")
        self.high_risk_categories = config.HIGH_RISK_MERCHANTS
        self.medium_risk_categories = config.MEDIUM_RISK_MERCHANTS
    
    def evaluate(self, transaction, db) -> Optional[Dict]:

        category = transaction.merchant_category.lower()
        

        if category in [c.lower() for c in self.high_risk_categories]:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'Transaction with high-risk merchant category: {transaction.merchant_category}'
            }
        

        elif category in [c.lower() for c in self.medium_risk_categories]:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'MEDIUM',
                'details': f'Transaction with medium-risk merchant category: {transaction.merchant_category}'
            }
        
        return None