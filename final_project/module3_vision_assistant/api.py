"""FastAPI endpoints for Module 3."""

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from vision_helper import describe_page, find_element

app = FastAPI(title="Vision Assistant API", version="1.0")


class DescribeRequest(BaseModel):
    url: str
    instruction: Optional[str] = None


class FindRequest(BaseModel):
    url: str
    query: str


@app.get("/")
def health_check():
    return {"status": "running", "module": "vision_assistant"}


@app.post("/vision/describe")
def describe_endpoint(req: DescribeRequest):
    return describe_page(req.url, instruction=req.instruction)


@app.post("/vision/find")
def find_endpoint(req: FindRequest):
    return find_element(req.url, req.query)
