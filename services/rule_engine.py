"""
Rule Engine

Coordinates evaluation of all rules against transactions.
This is the "brain" that runs all fraud detection rules.
"""

from typing import List, Dict
from rules.amount_threshold_rule import AmountThresholdRule
from rules.velocity_rule import VelocityRule
from rules.daily_limit_rule import DailyLimitRule
from rules.high_risk_merchant_rule import HighRiskMerchantRule
from rules.rapid_succession_rule import RapidSuccessionRule


class RuleEngine:
    """
    Manages and executes all monitoring rules
    
    Responsibilities:
    1. Maintains list of all active rules
    2. Runs each rule against transactions
    3. Collects and returns all alerts
    """
    
    def __init__(self):
        """
        Initialize rule engine with all active rules
        
        To add a new rule:
        1. Create the rule class
        2. Import it above
        3. Add it to self.rules list here
        """
        self.rules = [
            AmountThresholdRule(),
            VelocityRule(),
            DailyLimitRule(),
            HighRiskMerchantRule(),
            RapidSuccessionRule()
        ]
    
    def evaluate_transaction(self, transaction, db) -> List[Dict]:
        """
        Run all enabled rules against a transaction
        
        Args:
            transaction: Transaction object to evaluate
            db: Database object for rules that need historical data
        
        Returns:
            List of alert dictionaries (empty if no alerts)
        """
        alerts = []
        
        # Run each rule
        for rule in self.rules:
            # Skip disabled rules
            if not rule.is_enabled():
                continue
            
            # Evaluate rule
            result = rule.evaluate(transaction, db)
            
            # If rule triggered, add to alerts list
            if result and result.get('triggered'):
                alerts.append(result)
        
        return alerts
    
    def get_active_rules(self) -> List:
        """
        Get list of all enabled rules
        
        Returns:
            List of enabled rule objects
        """
        return [rule for rule in self.rules if rule.is_enabled()]
    
    def enable_rule(self, rule_name: str) -> bool:
        """
        Enable a specific rule by name
        
        Args:
            rule_name: Name of rule to enable
        
        Returns:
            True if rule found and enabled, False otherwise
        """
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enable()
                return True
        return False
    
    def disable_rule(self, rule_name: str) -> bool:
        """
        Disable a specific rule by name
        
        Args:
            rule_name: Name of rule to disable
        
        Returns:
            True if rule found and disabled, False otherwise
        """
        for rule in self.rules:
            if rule.name == rule_name:
                rule.disable()
                return True
        return False