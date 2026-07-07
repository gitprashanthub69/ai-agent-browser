"""FastAPI endpoints for memory operations."""

from fastapi import APIRouter
from pydantic import BaseModel

from .memory_store import (
    get_documents,
    get_form_history,
    get_notes,
    get_profile,
    save_document,
    save_form_history,
    save_note,
    save_task,
    search_history,
    set_profile_bulk,
)

router = APIRouter(tags=["Memory"])


class ProfilePayload(BaseModel):
    data: dict


class NotePayload(BaseModel):
    content: str
    title: str = ""
    source_url: str = ""
    tags: list[str] | None = None
    note_type: str = "summary"


class FormHistoryPayload(BaseModel):
    url: str
    form_title: str
    fields: list[dict]
    submitted: bool = True


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "module": "module6_memory"}


@router.get("/memory/profile")
def memory_profile() -> dict:
    return get_profile()


@router.post("/memory/profile")
def save_memory_profile(payload: ProfilePayload) -> dict:
    set_profile_bulk(payload.data)
    return get_profile()


@router.get("/memory/notes")
def memory_notes(limit: int = 20) -> list[dict]:
    return get_notes(limit=limit)


@router.post("/memory/notes")
def create_memory_note(payload: NotePayload) -> dict:
    note_id = save_note(payload.content, title=payload.title, source_url=payload.source_url, tags=payload.tags, note_type=payload.note_type)
    return {"id": note_id}


@router.get("/memory/contacts")
def memory_contacts() -> list[dict]:
    return []


@router.post("/memory/form-history")
def add_form_history(payload: FormHistoryPayload) -> dict:
    save_form_history(payload.url, payload.form_title, payload.fields, payload.submitted)
    return {"status": "saved"}


@router.get("/memory/search")
def memory_search(query: str) -> list[dict]:
    return search_history(query)


@router.get("/memory/context")
def memory_context() -> dict:
    return {"profile": get_profile(), "notes": get_notes(limit=5), "forms": get_form_history(limit=5)}
