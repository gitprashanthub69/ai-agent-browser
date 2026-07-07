"""
api.py
FastAPI endpoints for Module 4 - Calendar Assistant.
Run: uvicorn api:app --reload --port 8003
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

try:
    from .calendar_helper import list_upcoming_events, find_free_slots
    from .calendar_intent import schedule_from_text
except ImportError:  # pragma: no cover - allows direct script execution
    from calendar_helper import list_upcoming_events, find_free_slots
    from calendar_intent import schedule_from_text

app = FastAPI(title="Calendar Assistant API")


class ScheduleRequest(BaseModel):
    instruction: str
    confirm: bool = False


class FreeSlotRequest(BaseModel):
    date: str
    duration_minutes: Optional[int] = 30


@app.get("/")
def health():
    return {"status": "running", "module": "calendar_assistant"}


@app.get("/calendar/events")
def events(max_results: int = 10):
    return list_upcoming_events(max_results)


@app.post("/calendar/schedule")
def schedule(req: ScheduleRequest):
    return schedule_from_text(req.instruction, confirm=req.confirm)


@app.post("/calendar/free-slots")
def free_slots(req: FreeSlotRequest):
    return find_free_slots(req.date, req.duration_minutes)
