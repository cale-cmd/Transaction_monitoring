"""
Alert Manager

Handles creation, storage, and retrieval of security alerts.
"""

from typing import List, Optional
from models.alert import Alert
from datetime import datetime
import uuid


class AlertManager:
    """
    Manages security alerts
    
    Responsibilities:
    - Create alerts from rule results
    - Save alerts to database
    - Retrieve alerts with filtering
    - Update alert status (resolve, etc.)
    """
    
    def __init__(self, db):
        """
        Initialize alert manager
        
        Args:
            db: Database object
        """
        self.db = db
    
    def create_alert(self, transaction, rule_result: dict) -> Alert:
        """
        Create and save an alert
        
        Args:
            transaction: Transaction object that triggered the alert
            rule_result: Dictionary returned by rule.evaluate()
        
        Returns:
            Alert object
        """
        # Create alert object
        alert = Alert(
            alert_id=f"ALERT_{uuid.uuid4().hex[:12].upper()}",
            transaction_id=transaction.transaction_id,
            rule_name=rule_result['rule_name'],
            severity=rule_result['severity'],
            details=rule_result['details'],
            timestamp=datetime.now().isoformat(),
            status='OPEN'
        )
        
        # Save to database
        self.db.insert_alert(alert)
        
        return alert
    
    def get_alerts(self, status: str = None, severity: str = None) -> List[Alert]:
        """
        Retrieve alerts with optional filtering
        
        Args:
            status: Filter by status (OPEN, RESOLVED, FALSE_POSITIVE)
            severity: Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)
        
        Returns:
            List of Alert objects
        """
        # Get alerts from database
        alert_dicts = self.db.get_alerts(status=status, severity=severity)
        
        # Convert to Alert objects
        alerts = [Alert.from_dict(ad) for ad in alert_dicts]
        
        return alerts
    
    def get_alert_by_id(self, alert_id: str) -> Optional[Alert]:
        """
        Get a single alert by ID
        
        Args:
            alert_id: Alert ID to find
        
        Returns:
            Alert object or None if not found
        """
        results = self.db.execute_query(
            "SELECT * FROM alerts WHERE alert_id = ?",
            (alert_id,)
        )
        
        if results:
            return Alert.from_dict(results[0])
        return None
    
    def resolve_alert(self, alert_id: str, resolution: str, 
                     reviewed_by: str, notes: str = None) -> Optional[Alert]:
        """
        Mark an alert as resolved
        
        Args:
            alert_id: ID of alert to resolve
            resolution: Resolution status (APPROVED, REJECTED, FALSE_POSITIVE)
            reviewed_by: ID of person who reviewed
            notes: Optional notes about the resolution
        
        Returns:
            Updated Alert object, or None if alert not found
        """
        # Update database
        success = self.db.update_alert_status(
            alert_id=alert_id,
            status=resolution,
            resolved_by=reviewed_by,
            notes=notes
        )
        
        if success:
            return self.get_alert_by_id(alert_id)
        return None
    
    def get_alert_statistics(self) -> dict:
        """
        Get statistics about alerts
        
        Returns:
            Dictionary with alert statistics
        """
        all_alerts = self.db.execute_query("SELECT * FROM alerts")
        
        stats = {
            'total_alerts': len(all_alerts),
            'by_status': {},
            'by_severity': {},
            'by_rule': {}
        }
        
        # Count by status
        for alert in all_alerts:
            status = alert['status']
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
        
        # Count by severity
        for alert in all_alerts:
            severity = alert['severity']
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
        
        # Count by rule
        for alert in all_alerts:
            rule = alert['rule_name']
            stats['by_rule'][rule] = stats['by_rule'].get(rule, 0) + 1
        
        return stats