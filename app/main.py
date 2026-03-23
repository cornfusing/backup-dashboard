import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db import init_db, insert_event, fetch_logs, fetch_latest_for_source
from app.heartbeat import (
    is_overdue,
    get_backup_heartbeat_hours,
    get_restore_heartbeat_hours,
)
from app.models import EventIn
from app.notifier import send_discord_notification

load_dotenv()

app = FastAPI(title="Backup Dashboard")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/api/events")
def create_event(event: EventIn):
    ts = datetime.now(timezone.utc).isoformat()
    insert_event(ts, event.source, event.event, event.message)

    send_discord_notification(
        f"[{event.source.upper()}] {event.event} - {event.message or ''}".strip()
    )

    return {"ok": True, "timestamp": ts}


@app.get("/api/logs")
def get_logs(limit: int = Query(default=100, le=500), offset: int = 0):
    return fetch_logs(limit=limit, offset=offset)


@app.get("/api/status")
def get_status():
    backup = fetch_latest_for_source("backup")
    restore = fetch_latest_for_source("restore")

    return {
        "backup": {
            "latest_event": backup["event"] if backup else None,
            "latest_ts": backup["ts"] if backup else None,
            "message": backup["message"] if backup else None,
            "overdue": is_overdue(
                backup["ts"] if backup else None,
                get_backup_heartbeat_hours(),
            ),
        },
        "restore": {
            "latest_event": restore["event"] if restore else None,
            "latest_ts": restore["ts"] if restore else None,
            "message": restore["message"] if restore else None,
            "overdue": is_overdue(
                restore["ts"] if restore else None,
                get_restore_heartbeat_hours(),
            ),
        },
    }
