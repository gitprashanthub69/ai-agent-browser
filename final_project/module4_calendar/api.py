from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .calendar_client import CalendarClient

router = APIRouter(prefix="/api/calendar", tags=["Calendar"])

class EventCreate(BaseModel):
    summary: str
    start_time: str
    end_time: str
    description: str = ""

@router.get("/events")
async def list_events():
    try:
        client = CalendarClient()
        events = client.get_upcoming_events()
        return {"status": "success", "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events")
async def add_event(event: EventCreate):
    try:
        client = CalendarClient()
        res = client.create_event(event.summary, event.start_time, event.end_time, event.description)
        return {"status": "success", "event_link": res.get('htmlLink')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
