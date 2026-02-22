
from abc import ABC, abstractmethod
from typing import Optional, Dict


class BaseRule(ABC):

    
    def __init__(self, name: str):

        self.name = name
        self.enabled = True
    
    @abstractmethod
    def evaluate(self, transaction, db) -> Optional[Dict]:

        pass
    
    def is_enabled(self) -> bool:

        return self.enabled
    
    def enable(self):

        self.enabled = True
    
    def disable(self):

        self.enabled = False