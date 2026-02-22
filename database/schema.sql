-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    amount REAL NOT NULL,
    merchant_id TEXT NOT NULL,
    merchant_category TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    location TEXT,
    is_international INTEGER DEFAULT 0,
    merchant_country TEXT DEFAULT 'IN',
    created_at TEXT DEFAULT (datetime('now'))
);

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    alert_id TEXT PRIMARY KEY,
    transaction_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    severity TEXT NOT NULL,
    details TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT DEFAULT 'OPEN',
    resolved_at TEXT,
    resolved_by TEXT,
    resolution_notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_transactions_user_time ON transactions(user_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_transaction_id ON alerts(transaction_id);