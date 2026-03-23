import os
from datetime import datetime, timezone


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def is_overdue(latest_ts: str | None, hours: int) -> bool:
    if not latest_ts:
        return True
    last = parse_iso(latest_ts)
    now = datetime.now(timezone.utc)
    delta_hours = (now - last).total_seconds() / 3600
    return delta_hours > hours


def get_backup_heartbeat_hours() -> int:
    return int(os.getenv("BACKUP_HEARTBEAT_HOURS", "26"))


def get_restore_heartbeat_hours() -> int:
    return int(os.getenv("RESTORE_HEARTBEAT_HOURS", "192"))
