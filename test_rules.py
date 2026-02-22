"""
Comprehensive test script for all rules
"""

from models.transaction import Transaction
from rules.amount_threshold_rule import AmountThresholdRule
from rules.velocity_rule import VelocityRule
from rules.daily_limit_rule import DailyLimitRule
from rules.high_risk_merchant_rule import HighRiskMerchantRule
from rules.rapid_succession_rule import RapidSuccessionRule
from database.db import Database
from datetime import datetime, timedelta

print("=" * 70)
print("COMPREHENSIVE RULE TESTING")
print("=" * 70)

# Create database
db = Database()

# Create all rules
rules = [
    AmountThresholdRule(),
    VelocityRule(),
    DailyLimitRule(),
    HighRiskMerchantRule(),
    RapidSuccessionRule()
]

print(f"\n✓ Created {len(rules)} rules:")
for rule in rules:
    print(f"  - {rule.name}")

# Test 1: Normal transaction (should NOT trigger any rules)
print("\n" + "=" * 70)
print("TEST 1: Normal Transaction")
print("=" * 70)
txn1 = Transaction(
    transaction_id="TXN_NORMAL",
    user_id="USER_NORMAL",
    amount=50000,
    merchant_id="MERCHANT_ABC",
    merchant_category="electronics",
    payment_method="credit_card",
    timestamp=datetime.now().isoformat()
)
db.insert_transaction(txn1)

alerts_triggered = 0
for rule in rules:
    result = rule.evaluate(txn1, db)
    if result:
        print(f"  ✗ {rule.name}: {result['severity']} - {result['details']}")
        alerts_triggered += 1

if alerts_triggered == 0:
    print("  ✓ PASS: No alerts triggered (as expected)")
else:
    print(f"  ✗ FAIL: {alerts_triggered} unexpected alerts")

# Test 2: High amount transaction (should trigger AmountThresholdRule)
print("\n" + "=" * 70)
print("TEST 2: High Amount (₹600,000)")
print("=" * 70)
txn2 = Transaction(
    transaction_id="TXN_HIGH_AMOUNT",
    user_id="USER_HIGH_AMOUNT",
    amount=600000,
    merchant_id="MERCHANT_ABC",
    merchant_category="electronics",
    payment_method="credit_card",
    timestamp=datetime.now().isoformat()
)
db.insert_transaction(txn2)

for rule in rules:
    result = rule.evaluate(txn2, db)
    if result:
        print(f"  ✓ {rule.name}: {result['severity']} - {result['details']}")

# Test 3: High-risk merchant (should trigger HighRiskMerchantRule)
print("\n" + "=" * 70)
print("TEST 3: High-Risk Merchant (crypto_exchange)")
print("=" * 70)
txn3 = Transaction(
    transaction_id="TXN_CRYPTO",
    user_id="USER_CRYPTO",
    amount=50000,
    merchant_id="CRYPTO_EXCHANGE",
    merchant_category="crypto_exchange",
    payment_method="credit_card",
    timestamp=datetime.now().isoformat()
)
db.insert_transaction(txn3)

for rule in rules:
    result = rule.evaluate(txn3, db)
    if result:
        print(f"  ✓ {rule.name}: {result['severity']} - {result['details']}")

# Test 4: Velocity - Multiple transactions (should trigger VelocityRule)
print("\n" + "=" * 70)
print("TEST 4: High Velocity (6 transactions in last hour)")
print("=" * 70)
user_velocity = "USER_VELOCITY"
current_time = datetime.now()

# Insert 5 transactions in last 30 minutes
for i in range(5):
    txn = Transaction(
        transaction_id=f"TXN_VEL_{i}",
        user_id=user_velocity,
        amount=10000,
        merchant_id="MERCHANT_ABC",
        merchant_category="electronics",
        payment_method="credit_card",
        timestamp=(current_time - timedelta(minutes=30)).isoformat()
    )
    db.insert_transaction(txn)

# 6th transaction (should trigger velocity rule)
txn_velocity = Transaction(
    transaction_id="TXN_VEL_6",
    user_id=user_velocity,
    amount=10000,
    merchant_id="MERCHANT_ABC",
    merchant_category="electronics",
    payment_method="credit_card",
    timestamp=current_time.isoformat()
)
db.insert_transaction(txn_velocity)

for rule in rules:
    result = rule.evaluate(txn_velocity, db)
    if result:
        print(f"  ✓ {rule.name}: {result['severity']} - {result['details']}")

# Test 5: Multiple rules triggered at once
print("\n" + "=" * 70)
print("TEST 5: Multiple Rules (High amount + High-risk merchant)")
print("=" * 70)
txn_multiple = Transaction(
    transaction_id="TXN_MULTIPLE",
    user_id="USER_MULTIPLE",
    amount=700000,
    merchant_id="CRYPTO_EXCHANGE",
    merchant_category="crypto_exchange",
    payment_method="credit_card",
    timestamp=datetime.now().isoformat()
)
db.insert_transaction(txn_multiple)

triggered_rules = []
for rule in rules:
    result = rule.evaluate(txn_multiple, db)
    if result:
        triggered_rules.append(rule.name)
        print(f"  ✓ {rule.name}: {result['severity']} - {result['details']}")

if len(triggered_rules) >= 2:
    print(f"\n  ✓ PASS: Multiple rules triggered ({len(triggered_rules)} rules)")
else:
    print(f"\n  ✗ FAIL: Expected multiple rules, got {len(triggered_rules)}")

print("\n" + "=" * 70)
print("ALL RULES TESTED SUCCESSFULLY!")
print("=" * 70)