"""FastAPI endpoints for Module 2."""

from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

try:
    from .email_composer import draft_new_email, draft_reply
    from .email_reader import get_thread, list_recent_emails, summarize_thread
    from .email_sender import reply_to_thread, send_email, send_group_email
except ImportError:  # pragma: no cover - allows direct script execution
    from email_composer import draft_new_email, draft_reply
    from email_reader import get_thread, list_recent_emails, summarize_thread
    from email_sender import reply_to_thread, send_email, send_group_email

app = FastAPI(title="Email Assistant API", version="1.0")


class DraftRequest(BaseModel):
    instruction: str
    tone: Optional[str] = "professional"


class ReplyDraftRequest(BaseModel):
    thread_id: str
    instruction: str
    tone: Optional[str] = "professional"


class SendRequest(BaseModel):
    to: str
    subject: str
    body: str
    confirm: bool = False


class ReplyRequest(BaseModel):
    thread_id: str
    to: str
    subject: str
    body: str
    confirm: bool = False


class GroupSendRequest(BaseModel):
    recipients: List[str]
    subject: str
    body: str
    confirm: bool = False


@app.get("/")
def health_check():
    return {"status": "running", "module": "email_assistant"}


@app.get("/emails/recent")
def recent_emails(max_results: int = 10, query: str = ""):
    return list_recent_emails(max_results=max_results, query=query)


@app.get("/emails/thread/{thread_id}")
def thread_detail(thread_id: str):
    return get_thread(thread_id)


@app.get("/emails/thread/{thread_id}/summary")
def thread_summary(thread_id: str):
    return {"thread_id": thread_id, "summary": summarize_thread(thread_id)}


@app.post("/emails/draft")
def draft_email(req: DraftRequest):
    return draft_new_email(req.instruction, tone=req.tone)


@app.post("/emails/draft-reply")
def draft_reply_endpoint(req: ReplyDraftRequest):
    messages = get_thread(req.thread_id)
    return draft_reply(messages, req.instruction, tone=req.tone)


@app.post("/emails/send")
def send_endpoint(req: SendRequest):
    return send_email(req.to, req.subject, req.body, confirm=req.confirm)


@app.post("/emails/reply")
def reply_endpoint(req: ReplyRequest):
    return reply_to_thread(req.thread_id, req.to, req.subject, req.body, confirm=req.confirm)


@app.post("/emails/send-group")
def send_group_endpoint(req: GroupSendRequest):
    return send_group_email(req.recipients, req.subject, req.body, confirm=req.confirm)
