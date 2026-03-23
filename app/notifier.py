import os
import requests


def send_discord_notification(text: str):
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        return

    try:
        requests.post(webhook, json={"content": text}, timeout=10)
    except Exception:
        # Für MVP absichtlich still scheitern
        pass
