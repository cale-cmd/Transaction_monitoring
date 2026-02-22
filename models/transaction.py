"""
Transaction data model
Represents a financial transaction
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Transaction:
    """Represents a financial transaction"""
    
    transaction_id: str
    user_id: str
    amount: float
    merchant_id: str
    merchant_category: str
    payment_method: str
    timestamp: str
    location: Optional[str] = None
    is_international: bool = False
    merchant_country: str = "IN"
    
    def to_dict(self):
        """Convert transaction to dictionary format"""
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'merchant_id': self.merchant_id,
            'merchant_category': self.merchant_category,
            'payment_method': self.payment_method,
            'timestamp': self.timestamp,
            'location': self.location,
            'is_international': self.is_international,
            'merchant_country': self.merchant_country
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create transaction from dictionary"""
        return cls(
            transaction_id=data.get('transaction_id', f"TXN_{uuid.uuid4().hex[:12].upper()}"),
            user_id=data['user_id'],
            amount=float(data['amount']),
            merchant_id=data['merchant_id'],
            merchant_category=data['merchant_category'],
            payment_method=data['payment_method'],
            timestamp=data.get('timestamp', datetime.now().isoformat()),
            location=data.get('location'),
            is_international=data.get('is_international', False),
            merchant_country=data.get('merchant_country', 'IN')
        )
    
    def get_timestamp_obj(self):
        return datetime.fromisoformat(self.timestamp)