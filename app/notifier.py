import os
from datetime import datetime, timezone

import requests


def _event_color(event: str) -> int:
    event = event.lower()

    if "success" in event:
        return 0x2ECC71  # grün
    if "failed" in event:
        return 0xE74C3C  # rot
    if "started" in event:
        return 0xF1C40F  # gelb
    if "overdue" in event:
        return 0xE67E22  # orange

    return 0x3498DB  # blau fallback


def _pretty_title(source: str, event: str) -> str:
    source = source.capitalize()

    if "success" in event:
        emoji = "🟢"
        action = "successful"
    elif "failed" in event:
        emoji = "🔴"
        action = "failed"
    elif "started" in event:
        emoji = "🟡"
        action = "started"
    else:
        emoji = "🔵"
        action = event

    return f"{emoji} {source} {action}"


def send_discord_notification(source: str, event: str, message: str | None = None):
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        return

    timestamp = datetime.now(timezone.utc).isoformat()
    color = _event_color(event)

    embed = {
        "title": _pretty_title(source, event),
        "color": color,
        "fields": [
            {
                "name": "Source",
                "value": source,
                "inline": True,
            },
            {
                "name": "Event",
                "value": event,
                "inline": True,
            },
            {
                "name": "Message",
                "value": message if message else "—",
                "inline": False,
            },
        ],
        "footer": {
            "text": "Backup Dashboard",
        },
        "timestamp": timestamp,
    }

    payload = {
        "username": "Backup Monitor",
        "embeds": [embed],
    }

    try:
        response = requests.post(webhook, json=payload, timeout=10)
        response.raise_for_status()
    except Exception:
        # Für MVP bewusst still scheitern
        pass
