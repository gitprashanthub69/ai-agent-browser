from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .summariser import WebSummariser

router = APIRouter(prefix="/api/summary", tags=["Summariser"])
summariser = WebSummariser()

class SummaryRequest(BaseModel):
    url: str

@router.post("/")
async def generate_summary(req: SummaryRequest):
    try:
        result = await summariser.summarise_url(req.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
