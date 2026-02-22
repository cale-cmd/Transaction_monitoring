"""
Test script for services layer
"""

from database.db import Database
from services.rule_engine import RuleEngine
from services.alert_manager import AlertManager
from services.transaction_service import TransactionService
from datetime import datetime

print("=" * 70)
print("TESTING SERVICES LAYER")
print("=" * 70)

# Initialize all services
print("\n1. Initializing services...")
db = Database()
rule_engine = RuleEngine()
alert_manager = AlertManager(db)
transaction_service = TransactionService(db, rule_engine, alert_manager)
print("   ✓ All services initialized")

# Test Rule Engine
print("\n2. Testing Rule Engine...")
active_rules = rule_engine.get_active_rules()
print(f"   ✓ Active rules: {len(active_rules)}")
for rule in active_rules:
    print(f"     - {rule.name}")

# Test processing a normal transaction
print("\n3. Processing normal transaction...")
transaction_data = {
    'user_id': 'USER_SERVICE_TEST',
    'amount': 50000,
    'merchant_id': 'MERCHANT_ABC',
    'merchant_category': 'electronics',
    'payment_method': 'credit_card'
}

result = transaction_service.process_transaction(transaction_data)
print(f"   Transaction ID: {result['transaction_id']}")
print(f"   Status: {result['status']}")
print(f"   Alerts: {result['alert_count']}")

if result['status'] == 'APPROVED':
    print("   ✓ PASS: Normal transaction approved")
else:
    print("   ✗ FAIL: Normal transaction should be approved")

# Test processing suspicious transaction
print("\n4. Processing suspicious transaction...")
suspicious_data = {
    'user_id': 'USER_SUSPICIOUS',
    'amount': 700000,  # High amount
    'merchant_id': 'CRYPTO_EXCHANGE',
    'merchant_category': 'crypto_exchange',  # High-risk
    'payment_method': 'credit_card'
}

result2 = transaction_service.process_transaction(suspicious_data)
print(f"   Transaction ID: {result2['transaction_id']}")
print(f"   Status: {result2['status']}")
print(f"   Alerts: {result2['alert_count']}")

if result2['status'] == 'FLAGGED' and result2['alert_count'] >= 2:
    print("   ✓ PASS: Suspicious transaction flagged")
    for alert in result2['alerts']:
        print(f"     - {alert['rule_name']}: {alert['severity']}")
else:
    print("   ✗ FAIL: Suspicious transaction should be flagged")

# Test Alert Manager
print("\n5. Testing Alert Manager...")
all_alerts = alert_manager.get_alerts()
print(f"   Total alerts in database: {len(all_alerts)}")

open_alerts = alert_manager.get_alerts(status='OPEN')
print(f"   Open alerts: {len(open_alerts)}")

if len(open_alerts) > 0:
    print("   ✓ PASS: Alerts stored successfully")
else:
    print("   ✗ FAIL: Expected some open alerts")

# Test Alert Statistics
print("\n6. Testing Alert Statistics...")
stats = alert_manager.get_alert_statistics()
print(f"   Total alerts: {stats['total_alerts']}")
print(f"   By severity: {stats['by_severity']}")
print(f"   By rule: {stats['by_rule']}")

# Test retrieving transactions
print("\n7. Testing transaction retrieval...")
user_txns = transaction_service.get_transactions(user_id='USER_SERVICE_TEST')
print(f"   Found {len(user_txns)} transactions for USER_SERVICE_TEST")

if len(user_txns) > 0:
    print("   ✓ PASS: Transaction retrieval works")
else:
    print("   ✗ FAIL: Should find at least 1 transaction")

# Test user statistics
print("\n8. Testing user statistics...")
stats = transaction_service.get_user_statistics('USER_SERVICE_TEST')
print(f"   Total transactions: {stats['total_transactions']}")
print(f"   Total amount: ₹{stats['total_amount']:,.0f}")
print(f"   Average amount: ₹{stats['average_amount']:,.0f}")

print("\n" + "=" * 70)
print("SERVICES LAYER - ALL TESTS COMPLETE!")
print("=" * 70)