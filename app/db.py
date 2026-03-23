import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "events.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                source TEXT NOT NULL,
                event TEXT NOT NULL,
                message TEXT
            )
        """)
        conn.commit()


def insert_event(ts: str, source: str, event: str, message: str | None):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO events (ts, source, event, message) VALUES (?, ?, ?, ?)",
            (ts, source, event, message),
        )
        conn.commit()


def fetch_logs(limit: int = 100, offset: int = 0):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, ts, source, event, message
            FROM events
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]


def fetch_latest_for_source(source: str):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, ts, source, event, message
            FROM events
            WHERE source = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (source,),
        ).fetchone()
        return dict(row) if row else None
