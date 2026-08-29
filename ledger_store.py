import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path(__file__).with_name("audit_ledger.db")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")
SOP_CHECK_COLUMNS = frozenset(f"check_{index}" for index in range(1, 9))


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.executescript(SCHEMA_PATH.read_text())


def calculate_hesitation_cost(lag_seconds: float, burn_rate_per_sec: float = 0.7925) -> float:
    return round(lag_seconds * burn_rate_per_sec, 4)


def _parse_to_datetime(value) -> datetime:
    """Convert supported timestamp values to a naive UTC datetime."""
    if value is None:
        return datetime.utcnow()
    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(value)
    if isinstance(value, str):
        cleaned_value = value.replace(" UTC", "").replace("Z", "+00:00").strip()
        try:
            parsed_value = datetime.fromisoformat(cleaned_value)
        except ValueError:
            for format_string in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
                try:
                    parsed_value = datetime.strptime(cleaned_value, format_string)
                    break
                except ValueError:
                    continue
            else:
                return datetime.utcnow()
        if parsed_value.tzinfo is not None:
            return parsed_value.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed_value
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value
    return datetime.utcnow()


def record_ledger_entry(
    book: str,
    tier: int,
    actor_id: str,
    title: str,
    action: str,
    work_order_id: str,
    t0,
    blocker: str | None = None,
    notes: str | None = None,
):
    t0_dt = _parse_to_datetime(t0)
    t1_dt = datetime.utcnow()
    lag = max(0.0, (t1_dt - t0_dt).total_seconds())
    cost = calculate_hesitation_cost(lag)
    raw_payload = f"{book}|{tier}|{actor_id}|{title}|{action}|{work_order_id}|{t0_dt.isoformat()}|{t1_dt.isoformat()}|{lag}|{cost}"
    sha_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO forensic_ledger (
                operating_book, tier_level, actor_id, official_title, action_type,
                work_order_id, t0_detection, t1_resolution, governance_lag_sec,
                hesitation_cost, blocker_category, blocker_notes, sha256_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                book, tier, actor_id, title, action, work_order_id,
                t0_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                t1_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                lag, cost, blocker, notes, sha_hash,
            ),
        )


def get_or_create_sop_state(work_order_id: str, book: str):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM tier3_sop_state WHERE work_order_id = ?", (work_order_id,)
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO tier3_sop_state (work_order_id, operating_book) VALUES (?, ?)",
                (work_order_id, book),
            )
            row = conn.execute(
                "SELECT * FROM tier3_sop_state WHERE work_order_id = ?", (work_order_id,)
            ).fetchone()
        return dict(row)


def update_sop_check(work_order_id: str, check_col: str, value: int):
    if check_col not in SOP_CHECK_COLUMNS:
        raise ValueError(f"Unsupported SOP check column: {check_col}")

    with get_db() as conn:
        conn.execute(
            f"UPDATE tier3_sop_state SET {check_col} = ?, last_updated = CURRENT_TIMESTAMP "
            "WHERE work_order_id = ?",
            (int(bool(value)), work_order_id),
        )


def set_sop_blocker(work_order_id: str, blocker: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE tier3_sop_state SET active_blocker = ?, last_updated = CURRENT_TIMESTAMP "
            "WHERE work_order_id = ?",
            (blocker, work_order_id),
        )


def finalize_tier3_submission(work_order_id: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE tier3_sop_state SET is_submitted = 1, last_updated = CURRENT_TIMESTAMP "
            "WHERE work_order_id = ?",
            (work_order_id,),
        )