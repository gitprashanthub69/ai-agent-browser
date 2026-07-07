"""
api.py
FastAPI endpoints for Module 4 - Calendar Assistant.
Run: uvicorn api:app --reload --port 8003
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from .calendar_helper import list_upcoming_events, find_free_slots
from .calendar_intent import schedule_from_text

router = APIRouter(tags=["Calendar Assistant"])

class ScheduleRequest(BaseModel):
    instruction: str
    confirm: bool = False

class FreeSlotRequest(BaseModel):
    date: str
    duration_minutes: Optional[int] = 30

@router.get("/api/calendar/health")
def health():
    return {"status": "running", "module": "calendar_assistant"}

@router.get("/api/calendar/events")
def events(max_results: int = 10):
    return list_upcoming_events(max_results)

@router.post("/api/calendar/schedule")
def schedule(req: ScheduleRequest):
    return schedule_from_text(req.instruction, confirm=req.confirm)

@router.post("/api/calendar/free-slots")
def free_slots(req: FreeSlotRequest):
    return find_free_slots(req.date, req.duration_minutes)
