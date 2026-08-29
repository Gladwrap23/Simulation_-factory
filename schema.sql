CREATE TABLE IF NOT EXISTS forensic_ledger (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operating_book TEXT NOT NULL,
    tier_level INTEGER NOT NULL,
    actor_id TEXT NOT NULL,
    official_title TEXT NOT NULL,
    action_type TEXT NOT NULL,
    work_order_id TEXT NOT NULL,
    t0_detection TIMESTAMP NOT NULL,
    t1_resolution TIMESTAMP,
    governance_lag_sec REAL DEFAULT 0.0,
    hesitation_cost REAL DEFAULT 0.0,
    blocker_category TEXT,
    blocker_notes TEXT,
    sha256_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tier3_sop_state (
    work_order_id TEXT PRIMARY KEY,
    operating_book TEXT NOT NULL,
    check_1 INTEGER DEFAULT 0,
    check_2 INTEGER DEFAULT 0,
    check_3 INTEGER DEFAULT 0,
    check_4 INTEGER DEFAULT 0,
    check_5 INTEGER DEFAULT 0,
    check_6 INTEGER DEFAULT 0,
    check_7 INTEGER DEFAULT 0,
    check_8 INTEGER DEFAULT 0,
    active_blocker TEXT DEFAULT 'None',
    is_submitted INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);