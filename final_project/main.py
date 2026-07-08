import os
import uuid
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import create_db, get_session
from models import UserProfile, Task, AgentAction, TaskStatus
from agent_runner import run_agent_task

# Import routers from all modules
from module1_form_filler.api import router as form_router
from module2_email_assistant.api import router as email_router
from module3_vision_assistant.api import router as summary_router
from module4_calendar_assistant.api import router as calendar_router
from module6_memory.api import router as memory_router

active_connections: dict[str, list[WebSocket]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(title="AI Browser Agent Unified API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers
app.include_router(form_router)
app.include_router(email_router)
app.include_router(summary_router)
app.include_router(calendar_router)
app.include_router(memory_router)

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

@app.post("/command", summary="Send a natural language command to the agent")
async def post_command(payload: AgentAction, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    with get_session() as session:
        task = Task(id=task_id, command=payload.command, status=TaskStatus.pending, steps=[])
        session.add(task)
        session.commit()
    background_tasks.add_task(run_agent_task, task_id, payload.command, broadcast)
    return {"task_id": task_id, "status": "pending", "message": "Task started"}

@app.get("/status/{task_id}", summary="Get task progress")
def get_status(task_id: str):
    with get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"task_id": task.id, "command": task.command, "status": task.status, "steps": task.steps, "result": task.result}

@app.get("/user/profile", summary="Read user profile")
def get_profile():
    with get_session() as session:
        profile = session.exec(select(UserProfile)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="No profile found. POST to /user/profile first.")
        return profile

@app.post("/user/profile", summary="Create or update user profile")
def post_profile(profile_data: UserProfile):
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
    
    # Sync with Module 6 Memory Store
    try:
        from module6_memory.memory_store import set_profile_bulk
        set_profile_bulk(profile_data.model_dump() if hasattr(profile_data, "model_dump") else profile_data.dict())
    except Exception as e:
        print(f"Warning: Failed to sync profile with memory store: {e}")

    return {"message": "Profile saved successfully"}

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    if task_id not in active_connections:
        active_connections[task_id] = []
    active_connections[task_id].append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[task_id].remove(websocket)

@app.get("/")
def read_root():
    return {"message": "AI Browser Agent Backend Running"}
