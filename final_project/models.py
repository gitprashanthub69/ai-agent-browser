"""
Week 5 — Pydantic + SQLModel Data Models
These are the data contracts used across the API.
"""

from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, JSON, Column
from pydantic import BaseModel


# ── Enums ─────────────────────────────────────────────────────────────────────

class TaskStatus(str, Enum):
    pending   = "pending"
    running   = "running"
    completed = "completed"
    failed    = "failed"


# ── SQLModel tables (stored in SQLite) ────────────────────────────────────────

class UserProfile(SQLModel, table=True):
    """Stores user's personal info — agent reads this to fill forms."""
    id:          Optional[int] = Field(default=None, primary_key=True)
    name:        str           = Field(default="")
    email:       str           = Field(default="")
    phone:       str           = Field(default="")
    address:     str           = Field(default="")
    resume_text: str           = Field(default="")   # extracted from PDF


class Task(SQLModel, table=True):
    """Tracks each agent task from receipt to completion."""
    id:      str        = Field(primary_key=True)
    command: str        = Field(default="")
    status:  TaskStatus = Field(default=TaskStatus.pending)
    result:  str        = Field(default="")
    # JSON list of step strings e.g. ["✅ Navigated to google.com", "✅ Clicked search"]
    steps:   list       = Field(default=[], sa_column=Column(JSON))


# ── Pydantic request/response models ─────────────────────────────────────────

class AgentAction(BaseModel):
    """Request body for POST /command"""
    command: str


class StatusResponse(BaseModel):
    """Response for GET /status/{task_id}"""
    task_id: str
    command: str
    status:  TaskStatus
    steps:   list[str]
    result:  str
