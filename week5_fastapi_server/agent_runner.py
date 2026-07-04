"""
Week 5 — Agent Runner
Connects the Week 4 LangChain agent to FastAPI.
Runs as a background task, streams step updates via WebSocket broadcast.
"""

import sys
import os
import asyncio
from models import TaskStatus
from database import get_session
from sqlmodel import Session

# Add week4 to path so we can import its agent
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'week4_langchain_agent'))


async def run_agent_task(task_id: str, command: str, broadcast_fn):
    """
    Runs the LangChain agent for a given command.
    Updates the Task record in SQLite and broadcasts steps over WebSocket.
    """
    steps = []

    async def step(msg: str):
        steps.append(msg)
        await broadcast_fn(task_id, msg)
        # Update DB with latest steps
        with get_session() as session:
            from sqlmodel import select
            from models import Task
            task = session.get(Task, task_id)
            if task:
                task.steps = list(steps)
                task.status = TaskStatus.running
                session.add(task)
                session.commit()

    try:
        await step("🔄 Task received — starting agent...")

        # Import agent (uses Gemini via Week 4 code)
        try:
            from agent import build_agent
            agent = build_agent()
            await step("✅ Agent initialized")
        except Exception as e:
            await step(f"⚠️  Could not load Week 4 agent ({e}) — running in simulation mode")
            agent = None

        if agent:
            # Real agent run
            await step(f"🤖 Processing: {command}")
            result = agent.invoke({"input": command})
            output = result.get("output", "Done")
            await step(f"✅ Agent result: {output}")
        else:
            # Simulation mode — shows the pipeline working without live agent
            await step(f"📋 Parsing intent for: '{command}'")
            await asyncio.sleep(0.5)
            await step("🌐 Navigating to target...")
            await asyncio.sleep(0.5)
            await step("🖱️  Executing browser action...")
            await asyncio.sleep(0.5)
            await step("✅ Task completed (simulation mode)")
            output = "Completed in simulation mode"

        # Mark task complete in DB
        with get_session() as session:
            from models import Task
            task = session.get(Task, task_id)
            if task:
                task.status = TaskStatus.completed
                task.result = output
                task.steps = list(steps)
                session.add(task)
                session.commit()

        await broadcast_fn(task_id, "🏁 DONE")

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        await broadcast_fn(task_id, error_msg)

        with get_session() as session:
            from models import Task
            task = session.get(Task, task_id)
            if task:
                task.status = TaskStatus.failed
                task.result = error_msg
                task.steps = list(steps)
                session.add(task)
                session.commit()
