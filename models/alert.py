"""
Alert data model
Represents a security alert
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Alert:
    """Represents a security alert"""
    
    alert_id: str
    transaction_id: str
    rule_name: str
    severity: str
    details: str
    timestamp: str
    status: str = "OPEN"
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None
    
    def to_dict(self):
        """Convert alert to dictionary format"""
        return {
            'alert_id': self.alert_id,
            'transaction_id': self.transaction_id,
            'rule_name': self.rule_name,
            'severity': self.severity,
            'details': self.details,
            'timestamp': self.timestamp,
            'status': self.status,
            'resolved_at': self.resolved_at,
            'resolved_by': self.resolved_by,
            'resolution_notes': self.resolution_notes
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create alert from dictionary"""
        return cls(
            alert_id=data.get('alert_id', f"ALERT_{uuid.uuid4().hex[:12].upper()}"),
            transaction_id=data['transaction_id'],
            rule_name=data['rule_name'],
            severity=data['severity'],
            details=data['details'],
            timestamp=data.get('timestamp', datetime.now().isoformat()),
            status=data.get('status', 'OPEN'),
            resolved_at=data.get('resolved_at'),
            resolved_by=data.get('resolved_by'),
            resolution_notes=data.get('resolution_notes')
        )
    
    @classmethod
    def create_from_rule_result(cls, transaction_id: str, rule_result: dict):
        """Create alert from rule evaluation result"""
        return cls(
            alert_id=f"ALERT_{uuid.uuid4().hex[:12].upper()}",
            transaction_id=transaction_id,
            rule_name=rule_result['rule_name'],
            severity=rule_result['severity'],
            details=rule_result['details'],
            timestamp=datetime.now().isoformat()
        )