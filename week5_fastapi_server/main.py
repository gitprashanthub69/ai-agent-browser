"""
Week 5 — FastAPI Backend Server
Endpoints:
  POST /command          — receive text command, return task_id
  GET  /status/{task_id} — return task progress
  GET  /user/profile     — read user profile
  POST /user/profile     — write/update user profile
  WS   /ws/{task_id}     — stream live agent status updates
"""

import os
import uuid
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from models import UserProfile, Task, AgentAction, TaskStatus
from database import create_db, get_session
from agent_runner import run_agent_task

# ── In-memory store for active WebSocket connections ──────────────────────────
active_connections: dict[str, list[WebSocket]] = {}

# ── App startup ───────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()   # create SQLite tables on startup
    yield

app = FastAPI(
    title="AI Browser Agent API",
    description="Backend server for the Agentic AI Browser Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Helper: broadcast to all WebSocket clients for a task ─────────────────────

async def broadcast(task_id: str, message: str):
    if task_id in active_connections:
        dead = []
        for ws in active_connections[task_id]:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            active_connections[task_id].remove(ws)


# ── POST /command ─────────────────────────────────────────────────────────────

@app.post("/command", summary="Send a natural language command to the agent")
async def post_command(payload: AgentAction, background_tasks: BackgroundTasks):
    """
    Receives a text command, creates a task record, kicks off the agent
    as a background task, and immediately returns a task_id.
    """
    task_id = str(uuid.uuid4())

    with get_session() as session:
        task = Task(
            id=task_id,
            command=payload.command,
            status=TaskStatus.pending,
            steps=[],
        )
        session.add(task)
        session.commit()

    # Run agent in background so the response returns immediately
    background_tasks.add_task(run_agent_task, task_id, payload.command, broadcast)

    return {"task_id": task_id, "status": "pending", "message": "Task started"}


# ── GET /status/{task_id} ─────────────────────────────────────────────────────

@app.get("/status/{task_id}", summary="Get task progress")
def get_status(task_id: str):
    """Returns the current status and step log for a given task."""
    with get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {
            "task_id": task.id,
            "command": task.command,
            "status": task.status,
            "steps": task.steps,
            "result": task.result,
        }


# ── GET /user/profile ─────────────────────────────────────────────────────────

@app.get("/user/profile", summary="Read user profile")
def get_profile():
    """Returns the stored user profile (used by agent to fill forms)."""
    with get_session() as session:
        profile = session.exec(select(UserProfile)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="No profile found. POST to /user/profile first.")
        return profile


# ── POST /user/profile ────────────────────────────────────────────────────────

@app.post("/user/profile", summary="Create or update user profile")
def post_profile(profile_data: UserProfile):
    """Saves or replaces the user profile in SQLite."""
    with get_session() as session:
        existing = session.exec(select(UserProfile)).first()
        if existing:
            existing.name = profile_data.name
            existing.email = profile_data.email
            existing.phone = profile_data.phone
            existing.address = profile_data.address
            existing.resume_text = profile_data.resume_text
            session.add(existing)
        else:
            session.add(profile_data)
        session.commit()
    return {"message": "Profile saved successfully"}


# ── WebSocket /ws/{task_id} ───────────────────────────────────────────────────

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """
    Streams real-time agent step updates to the client.
    The agent_runner calls broadcast() after each step.
    """
    await websocket.accept()
    if task_id not in active_connections:
        active_connections[task_id] = []
    active_connections[task_id].append(websocket)

    try:
        while True:
            # Block until client sends text or disconnects (0 CPU overhead)
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[task_id].remove(websocket)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/", summary="Health check")
def root():
    return {"status": "running", "docs": "/docs"}
