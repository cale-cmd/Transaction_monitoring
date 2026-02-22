"""
Base class for all monitoring rules

All specific rules inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class BaseRule(ABC):
    """
    Abstract base class for all monitoring rules
    
    Every rule must implement the evaluate() method.
    """
    
    def __init__(self, name: str):
        """
        Initialize rule with a name
        
        Args:
            name: Unique identifier for this rule
        """
        self.name = name
        self.enabled = True
    
    @abstractmethod
    def evaluate(self, transaction, db) -> Optional[Dict]:
        """
        Evaluate the rule against a transaction
        
        Args:
            transaction: Transaction object to check
            db: Database object for querying historical data
        
        Returns:
            Dictionary with alert details if rule triggered:
            {
                'triggered': True,
                'rule_name': 'RULE_NAME',
                'severity': 'HIGH',
                'details': 'Human readable explanation'
            }
            
            Or None if rule did not trigger
        """
        pass
    
    def is_enabled(self) -> bool:
        """Check if rule is enabled"""
        return self.enabled
    
    def enable(self):
        """Enable this rule"""
        self.enabled = True
    
    def disable(self):
        """Disable this rule"""
        self.enabled = False