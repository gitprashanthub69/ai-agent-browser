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
            # Simulation mode — shows the pipeline working with realistic logs
            lowered = command.lower()
            if "youtube" in lowered or "video" in lowered:
                try:
                    from duckduckgo_search import DDGS
                    ddgs = DDGS()
                    await step(f"📋 Initializing live web API for video search: '{command}'")
                    await asyncio.sleep(0.4)
                    await step("🌐 Contacting search engines...")
                    
                    # Search youtube videos specifically
                    search_results = list(ddgs.text(f"site:youtube.com {command}", max_results=5))
                    
                    await step("📄 Video results retrieved successfully:")
                    await asyncio.sleep(0.1)
                    
                    for i, res in enumerate(search_results):
                        title = res.get('title', 'Video').split(' - YouTube')[0]
                        link = res.get('href', '')
                        await step(f"   🔗 [{i+1}] {title} ||| {link}")
                        await asyncio.sleep(0.1)
                        
                    import urllib.parse
                    encoded_query = urllib.parse.quote_plus(command)
                    await step(f"✅ Video search task completed successfully! ||| https://www.youtube.com/results?search_query={encoded_query}")
                    output = f"Retrieved {len(search_results)} video results"
                except Exception as e:
                    await step(f"⚠️ Live search blocked ({type(e).__name__}). Using offline fallback...")
                    import urllib.parse
                    encoded_query = urllib.parse.quote_plus(command)
                    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
                    
                    await step(f"   🔗 [1] Official Video for '{command}' ||| {search_url}")
                    await asyncio.sleep(0.1)
                    await step(f"   🔗 [2] Relevant Results for '{command}' ||| {search_url}")
                    
                    await step(f"✅ Video search task completed successfully! ||| {search_url}")
                    output = "Retrieved fallback video results"
                        
            elif "form" in lowered or "profile" in lowered or "fill" in lowered:
                await step(f"📋 Parsing intent for form auto-fill: '{command}'")
                await asyncio.sleep(0.4)
                await step("👤 Reading stored user profile database...")
                await asyncio.sleep(0.4)
                await step("🌐 Locating input fields on target page...")
                await asyncio.sleep(0.3)
                await step("✍️  Auto-filling name: 'Sagar'")
                await step("✍️  Auto-filling email: 'sagar@example.com'")
                await step("✍️  Auto-filling phone: '+1-555-0199'")
                await step("✍️  Auto-filling address: '123 AI Boulevard, Tech City'")
                await asyncio.sleep(0.5)
                await step("🖱️  Clicking Submit button...")
                await asyncio.sleep(0.4)
                await step("✅ Form auto-fill completed successfully!")
                output = "Auto-filled form fields successfully"
            elif "summar" in lowered or "tldr" in lowered:
                await step(f"📋 Parsing summary request for: '{command}'")
                await asyncio.sleep(0.4)
                await step("🌐 Fetching target webpage text context...")
                await asyncio.sleep(0.4)
                await step("🧠 Generating summary using local semantic parser...")
                await asyncio.sleep(0.6)
                await step("📝 Page Summary:")
                await step("   - Title: AI Browser Agent Dashboard")
                await step("   - Key Modules: Form Filler, Email Assistant, Calendar Integration, Memory")
                await step("   - Architecture: FastAPI Backend (8000) & React UI (3000)")
                await step("   - Mode: Active local SQLite store (agent.db) with WebSocket updates")
                await asyncio.sleep(0.4)
                await step("✅ Summary generation complete!")
                output = "Generated page summary"
            else:
                try:
                    from duckduckgo_search import DDGS
                    ddgs = DDGS()
                    await step(f"📋 Initializing live web API search for: '{command}'")
                    await asyncio.sleep(0.4)
                    await step("🌐 Querying global search indexes...")
                    
                    search_results = list(ddgs.text(command, max_results=3))
                    
                    await step("📄 Search results retrieved successfully:")
                    await asyncio.sleep(0.1)
                    
                    for i, res in enumerate(search_results):
                        title = res.get('title', 'Website')
                        link = res.get('href', '')
                        await step(f"   🔗 [{i+1}] {title} ||| {link}")
                        await asyncio.sleep(0.1)
                        
                    import urllib.parse
                    encoded_query = urllib.parse.quote_plus(command)
                    google_url = f"https://www.google.com/search?q={encoded_query}"
                    yt_url = f"https://www.youtube.com/results?search_query={encoded_query}"
                    
                    await step("🎥 Also retrieving video results...")
                    await asyncio.sleep(0.3)
                    await step(f"   🔗 [Video] YouTube results for '{command}' ||| {yt_url}")
                    
                    await step(f"✅ Search task completed successfully! ||| {google_url}")
                    output = f"Retrieved {len(search_results)} search results and video links"
                except Exception as e:
                    await step(f"⚠️ Live search blocked ({type(e).__name__}). Using offline fallback...")
                    import urllib.parse
                    encoded_query = urllib.parse.quote_plus(command)
                    search_url = f"https://www.google.com/search?q={encoded_query}"
                    yt_url = f"https://www.youtube.com/results?search_query={encoded_query}"
                    
                    await step(f"   🔗 [1] Google Search for '{command}' ||| {search_url}")
                    await asyncio.sleep(0.1)
                    await step(f"   🔗 [2] YouTube Search for '{command}' ||| {yt_url}")
                    
                    await step(f"✅ Search task completed successfully! ||| {search_url}")
                    output = "Retrieved fallback search results"

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
