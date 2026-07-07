"""
calendar_helper.py
Google Calendar integration: list events, create events, find free slots.
Reuses the same credentials.json from Module 2 (just needs Calendar scope added).
"""

import os
import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "calendar_token.json"
CREDENTIAL_CANDIDATES = [
    BASE_DIR / "credentials.json",
    BASE_DIR.parent / "module2_email_assistant" / "credentials.json",
    BASE_DIR.parent.parent / "credentials.json",
    BASE_DIR.parent.parent / "module2_email_assistant" / "credentials.json",
]


def resolve_credentials_file():
    for path in CREDENTIAL_CANDIDATES:
        if path.exists():
            return path
    return CREDENTIAL_CANDIDATES[0]


def get_calendar_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_path = resolve_credentials_file()
            if not creds_path.exists():
                raise FileNotFoundError(
                    "credentials.json missing. Reuse the one from Module 2, "
                    "just make sure Calendar API is enabled in Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def list_upcoming_events(max_results=10):
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    result = service.events().list(
        calendarId="primary", timeMin=now, maxResults=max_results,
        singleEvents=True, orderBy="startTime"
    ).execute()

    events = []
    for e in result.get("items", []):
        start = e["start"].get("dateTime", e["start"].get("date"))
        events.append({"id": e["id"], "summary": e.get("summary", "(no title)"), "start": start})
    return events


def create_event(summary, start_iso, end_iso, description="", attendees=None):
    """
    start_iso / end_iso example: "2026-07-10T15:00:00+05:30"
    attendees: optional list of email strings
    """
    service = get_calendar_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_iso},
        "end": {"dateTime": end_iso},
    }
    if attendees:
        event["attendees"] = [{"email": a} for a in attendees]

    created = service.events().insert(calendarId="primary", body=event).execute()
    return {"id": created["id"], "link": created.get("htmlLink")}


def find_free_slots(date_iso, duration_minutes=30, work_start=9, work_end=18):
    """
    Very simple free-slot finder for one day.
    date_iso example: "2026-07-10"
    Returns list of (start, end) ISO strings that are free.
    """
    service = get_calendar_service()
    day_start = f"{date_iso}T{work_start:02d}:00:00Z"
    day_end = f"{date_iso}T{work_end:02d}:00:00Z"

    busy = service.freebusy().query(body={
        "timeMin": day_start, "timeMax": day_end,
        "items": [{"id": "primary"}]
    }).execute()

    busy_slots = busy["calendars"]["primary"]["busy"]

    free = []
    cursor = datetime.datetime.fromisoformat(day_start.replace("Z", "+00:00"))
    end_of_day = datetime.datetime.fromisoformat(day_end.replace("Z", "+00:00"))
    delta = datetime.timedelta(minutes=duration_minutes)

    busy_ranges = [
        (datetime.datetime.fromisoformat(b["start"].replace("Z", "+00:00")),
         datetime.datetime.fromisoformat(b["end"].replace("Z", "+00:00")))
        for b in busy_slots
    ]

    while cursor + delta <= end_of_day:
        slot_end = cursor + delta
        overlaps = any(s < slot_end and e > cursor for s, e in busy_ranges)
        if not overlaps:
            free.append((cursor.isoformat(), slot_end.isoformat()))
        cursor += delta

    return free


if __name__ == "__main__":
    print("Upcoming events:")
    for e in list_upcoming_events(5):
        print(f"- {e['summary']} at {e['start']}")
