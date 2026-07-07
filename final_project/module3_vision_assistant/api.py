"""FastAPI endpoints for Module 3."""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .vision_helper import describe_page, find_element
from .summariser import WebSummariser

router = APIRouter(tags=["Vision & Summary"])

class DescribeRequest(BaseModel):
    url: str
    instruction: Optional[str] = None

class FindRequest(BaseModel):
    url: str
    query: str

class SummaryRequest(BaseModel):
    url: str
    focus: Optional[str] = None

@router.get("/api/vision/health")
def health_check():
    return {"status": "running", "module": "vision_assistant"}

@router.post("/api/vision/describe")
def describe_endpoint(req: DescribeRequest):
    return describe_page(req.url, instruction=req.instruction)

@router.post("/api/vision/find")
def find_endpoint(req: FindRequest):
    return find_element(req.url, req.query)

@router.post("/api/summary/")
async def summarize_page(req: SummaryRequest):
    try:
        summariser = WebSummariser()
        result = await summariser.summarise_url(req.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

