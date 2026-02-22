
from typing import List, Optional
from models.alert import Alert
from datetime import datetime
import uuid


class AlertManager:

    def __init__(self, db):

        self.db = db
    
    def create_alert(self, transaction, rule_result: dict) -> Alert:

        alert = Alert(
            alert_id=f"ALERT_{uuid.uuid4().hex[:12].upper()}",
            transaction_id=transaction.transaction_id,
            rule_name=rule_result['rule_name'],
            severity=rule_result['severity'],
            details=rule_result['details'],
            timestamp=datetime.now().isoformat(),
            status='OPEN'
        )
        

        self.db.insert_alert(alert)
        
        return alert
    
    def get_alerts(self, status: str = None, severity: str = None) -> List[Alert]:

        alert_dicts = self.db.get_alerts(status=status, severity=severity)
        

        alerts = [Alert.from_dict(ad) for ad in alert_dicts]
        
        return alerts
    
    def get_alert_by_id(self, alert_id: str) -> Optional[Alert]:

        results = self.db.execute_query(
            "SELECT * FROM alerts WHERE alert_id = ?",
            (alert_id,)
        )
        
        if results:
            return Alert.from_dict(results[0])
        return None
    
    def resolve_alert(self, alert_id: str, resolution: str, 
                     reviewed_by: str, notes: str = None) -> Optional[Alert]:

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