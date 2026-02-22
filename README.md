# Transaction Monitoring API

A real-time financial transaction monitoring system that detects suspicious activity using rule-based alerts.

##  Project Overview

This system monitors financial transactions and flags suspicious patterns that could indicate fraud or money laundering. It implements multiple detection rules including amount thresholds, transaction velocity, daily limits, high-risk merchants, and rapid succession patterns.


##  Features

- **Real-time transaction monitoring** with sub-second response times
- **5 fraud detection rules:**
  - Amount Threshold (flags large transactions)
  - Velocity (detects too many transactions in short time)
  - Daily Limit (tracks cumulative spending)
  - High-Risk Merchant (flags risky categories)
  - Rapid Succession (detects transactions within seconds)
- **RESTful API** for transaction processing and alert management
- **SQLite database** with optimized indexes
- **Audit logging** for compliance
- **Alert resolution workflow** for compliance teams
- **Daily reporting** with statistics

##  Prerequisites

- Python 3.8+
- pip (Python package manager)

##  Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd transaction-monitoring-api
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Activate on Mac/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

The API will start on `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Create Transaction
```bash
POST /api/transactions

Body:
{
  "user_id": "USER_123",
  "amount": 50000,
  "merchant_id": "MERCHANT_ABC",
  "merchant_category": "electronics",
  "payment_method": "credit_card"
}
```

### Get All Transactions
```bash
GET /api/transactions
GET /api/transactions?user_id=USER_123
```

### Get Specific Transaction
```bash
GET /api/transactions/{transaction_id}
```

### Get Alerts
```bash
GET /api/alerts
GET /api/alerts?status=OPEN&severity=HIGH
```

### Resolve Alert
```bash
PUT /api/alerts/{alert_id}/resolve

Body:
{
  "resolution": "APPROVED",
  "reviewed_by": "COMPLIANCE_OFFICER_001",
  "notes": "Verified with customer"
}
```

### Daily Report
```bash
GET /api/reports/daily
GET /api/reports/daily?date=2026-01-26
```

##  Testing

Run unit tests:
```bash
pytest tests/test_rules.py -v
```

Run API integration tests:
```bash
pytest tests/test_api.py -v
```

Run all tests:
```bash
pytest tests/ -v
```

##  Example Usage

### Example 1: Normal Transaction (Approved)
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER_001",
    "amount": 5000,
    "merchant_id": "AMAZON_IN",
    "merchant_category": "electronics",
    "payment_method": "credit_card"
  }'

Response:
{
  "transaction_id": "TXN_ABC123",
  "status": "APPROVED",
  "alerts": [],
  "alert_count": 0
}
```

### Example 2: Suspicious Transaction (Flagged)
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER_002",
    "amount": 600000,
    "merchant_id": "CRYPTO_EXCHANGE",
    "merchant_category": "crypto_exchange",
    "payment_method": "credit_card"
  }'

Response:
{
  "transaction_id": "TXN_XYZ789",
  "status": "FLAGGED",
  "alerts": [
    {
      "alert_id": "ALERT_001",
      "rule_name": "AMOUNT_THRESHOLD",
      "severity": "HIGH",
      "details": "Amount ₹600,000 exceeds high threshold of ₹500,000"
    },
    {
      "alert_id": "ALERT_002",
      "rule_name": "HIGH_RISK_MERCHANT",
      "severity": "HIGH",
      "details": "Transaction with high-risk merchant category: crypto_exchange"
    }
  ],
  "alert_count": 2
}
```

##  Configuration

Edit `config.py` to adjust thresholds:
```python
# Amount thresholds
AMOUNT_THRESHOLD_MEDIUM = 200000  # ₹2 lakhs
AMOUNT_THRESHOLD_HIGH = 500000    # ₹5 lakhs

# Velocity limits
VELOCITY_MAX_PER_HOUR = 5
VELOCITY_MAX_PER_DAY = 10

# Daily spending limits
DAILY_LIMIT_MEDIUM = 500000   # ₹5 lakhs
DAILY_LIMIT_HIGH = 1000000    # ₹10 lakhs
```

##  Rules Implemented

1. **Amount Threshold Rule**
   - Flags transactions above ₹2L (MEDIUM) or ₹5L (HIGH)
   - Detects unusually large payments

2. **Velocity Rule**
   - Flags >5 transactions/hour or >10 transactions/day
   - Detects rapid card usage (stolen card indicator)

3. **Daily Limit Rule**
   - Flags cumulative spending >₹5L or ₹10L in 24 hours
   - Detects money laundering via "structuring"

4. **High-Risk Merchant Rule**
   - Flags transactions with crypto exchanges, gambling, etc.
   - Categories commonly used for money laundering

5. **Rapid Succession Rule**
   - Flags multiple transactions within 60 seconds
   - Detects automated bot attacks






