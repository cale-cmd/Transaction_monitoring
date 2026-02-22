"""
Database connection and utilities
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import os
import config


class Database:
    """Database handler for SQLite"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        self.db_path = db_path or config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an INSERT, UPDATE, or DELETE query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.rowcount
    
    def insert_transaction(self, transaction) -> bool:
        """Insert a transaction into the database"""
        query = """
        INSERT INTO transactions (
            transaction_id, user_id, amount, merchant_id, 
            merchant_category, payment_method, timestamp,
            location, is_international, merchant_country
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            transaction.transaction_id,
            transaction.user_id,
            transaction.amount,
            transaction.merchant_id,
            transaction.merchant_category,
            transaction.payment_method,
            transaction.timestamp,
            transaction.location,
            1 if transaction.is_international else 0,
            transaction.merchant_country
        )
        
        self.execute_update(query, params)
        return True
    
    def insert_alert(self, alert) -> bool:
        """Insert an alert into the database"""
        query = """
        INSERT INTO alerts (
            alert_id, transaction_id, rule_name, severity,
            details, timestamp, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            alert.alert_id,
            alert.transaction_id,
            alert.rule_name,
            alert.severity,
            alert.details,
            alert.timestamp,
            alert.status
        )
        
        self.execute_update(query, params)
        return True
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """Get a single transaction by ID"""
        query = "SELECT * FROM transactions WHERE transaction_id = ?"
        results = self.execute_query(query, (transaction_id,))
        return results[0] if results else None
    
    def get_user_transactions_in_window(self, user_id: str, start_time: str, end_time: str = None) -> List[Dict]:
        """Get all transactions by a user within a time window"""
        if end_time:
            query = """
            SELECT * FROM transactions 
            WHERE user_id = ? AND timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp DESC
            """
            return self.execute_query(query, (user_id, start_time, end_time))
        else:
            query = """
            SELECT * FROM transactions 
            WHERE user_id = ? AND timestamp >= ?
            ORDER BY timestamp DESC
            """
            return self.execute_query(query, (user_id, start_time))
    
    def get_alerts(self, status: str = None, severity: str = None) -> List[Dict]:
        """Get alerts with optional filtering"""
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        
        query += " ORDER BY timestamp DESC"
        
        return self.execute_query(query, tuple(params) if params else None)
    
    def update_alert_status(self, alert_id: str, status: str, 
                           resolved_by: str = None, notes: str = None) -> bool:
        """Update an alert's status"""
        from datetime import datetime
        
        query = """
        UPDATE alerts 
        SET status = ?, resolved_at = ?, resolved_by = ?, resolution_notes = ?
        WHERE alert_id = ?
        """
        
        params = (
            status,
            datetime.now().isoformat() if status != 'OPEN' else None,
            resolved_by,
            notes,
            alert_id
        )
        
        self.execute_update(query, params)
        return True