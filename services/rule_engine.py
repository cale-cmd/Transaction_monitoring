
from typing import List, Dict
from rules.amount_threshold_rule import AmountThresholdRule
from rules.velocity_rule import VelocityRule
from rules.daily_limit_rule import DailyLimitRule
from rules.high_risk_merchant_rule import HighRiskMerchantRule
from rules.rapid_succession_rule import RapidSuccessionRule


class RuleEngine:

    def __init__(self):

        self.rules = [
            AmountThresholdRule(),
            VelocityRule(),
            DailyLimitRule(),
            HighRiskMerchantRule(),
            RapidSuccessionRule()
        ]
    
    def evaluate_transaction(self, transaction, db) -> List[Dict]:

        alerts = []
        

        for rule in self.rules:

            if not rule.is_enabled():
                continue
            

            result = rule.evaluate(transaction, db)
            

            if result and result.get('triggered'):
                alerts.append(result)
        
        return alerts
    
    def get_active_rules(self) -> List:

        return [rule for rule in self.rules if rule.is_enabled()]
    
    def enable_rule(self, rule_name: str) -> bool:

        for rule in self.rules:
            if rule.name == rule_name:
                rule.enable()
                return True
        return False
    
    def disable_rule(self, rule_name: str) -> bool:

        for rule in self.rules:
            if rule.name == rule_name:
                rule.disable()
                return True
        return False