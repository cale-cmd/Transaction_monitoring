"""
High-Risk Merchant Category Rule

Flags transactions with merchants in high-risk categories.
Certain merchant types are commonly used for money laundering.
"""

from rules.base_rule import BaseRule
from typing import Optional, Dict
import config


class HighRiskMerchantRule(BaseRule):
    """
    Checks if merchant category is high-risk
    
    Logic:
    - If merchant_category in HIGH_RISK list → HIGH alert
    - If merchant_category in MEDIUM_RISK list → MEDIUM alert
    - Otherwise → No alert
    """
    
    def __init__(self):
        super().__init__("HIGH_RISK_MERCHANT")
        self.high_risk_categories = config.HIGH_RISK_MERCHANTS
        self.medium_risk_categories = config.MEDIUM_RISK_MERCHANTS
    
    def evaluate(self, transaction, db) -> Optional[Dict]:
        """
        Check if merchant category is risky
        
        Args:
            transaction: Transaction object
            db: Database object (not used by this rule)
        
        Returns:
            Alert details if triggered, None otherwise
        """
        category = transaction.merchant_category.lower()
        
        # Check HIGH risk categories
        if category in [c.lower() for c in self.high_risk_categories]:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'HIGH',
                'details': f'Transaction with high-risk merchant category: {transaction.merchant_category}'
            }
        
        # Check MEDIUM risk categories
        elif category in [c.lower() for c in self.medium_risk_categories]:
            return {
                'triggered': True,
                'rule_name': self.name,
                'severity': 'MEDIUM',
                'details': f'Transaction with medium-risk merchant category: {transaction.merchant_category}'
            }
        
        return None