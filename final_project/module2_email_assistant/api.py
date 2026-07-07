from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .email_reader import list_recent_emails
from .email_composer import draft_new_email
from .email_sender import send_email

router = APIRouter(prefix="/api/email", tags=["Email"])

class EmailDraft(BaseModel):
    to: str
    subject: str
    context: str

@router.get("/inbox")
async def get_inbox():
    try:
        emails = list_recent_emails(max_results=5)
        return {"status": "success", "emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/draft")
async def draft_email(req: EmailDraft):
    try:
        draft = draft_new_email(req.context)
        return {"status": "success", "draft": draft}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send")
async def send_mail(req: EmailDraft):
    try:
        res = send_email(req.to, req.subject, req.context, confirm=True)
        return {"status": "success", "message": "Email sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
