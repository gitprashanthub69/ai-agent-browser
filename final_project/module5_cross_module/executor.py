"""Execute parsed cross-module steps in order, passing results forward."""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Optional

BASE = Path(__file__).resolve().parents[1]
for folder in [
    BASE / "module1_form_filler",
    BASE / "module2_email_assistant",
    BASE / "module4_calendar_assistant",
    BASE / "module6_memory",
]:
    if str(folder) not in sys.path:
        sys.path.append(str(folder))


class CrossModuleExecutor:
    def __init__(self, page=None, on_step=None) -> None:
        self.page = page
        self.on_step = on_step or self._default_on_step
        self.results: dict[int, Any] = {}

    async def execute(self, steps: list[dict]) -> dict:
        if not steps or (len(steps) == 1 and "error" in steps[0]):
            return {"success": False, "error": "No steps to execute"}

        summary = []
        for step in steps:
            step_num = step.get("step", len(summary) + 1)
            module = step.get("module", "")
            action = step.get("action", "")
            description = step.get("description", "")
            params = dict(step.get("params", {}) or {})
            depends_on = step.get("depends_on")
            if depends_on is not None and depends_on in self.results:
                params["_prev_result"] = self.results[depends_on]

            await self.on_step(step_num, module, description, "running", None)
            try:
                result = await self._run_step(module, action, params)
                self.results[step_num] = result
                await self.on_step(step_num, module, description, "done", result)
                summary.append({"step": step_num, "module": module, "action": action, "status": "done", "result": result})
            except Exception as exc:
                await self.on_step(step_num, module, description, "error", str(exc))
                summary.append({"step": step_num, "module": module, "action": action, "status": "error", "error": str(exc)})

        return {"success": all(item["status"] == "done" for item in summary), "steps": summary}

    async def _run_step(self, module: str, action: str, params: dict) -> Any:
        if module == "form":
            from form_filler import FormFiller
            if action == "fill":
                if self.page is None:
                    return {"status": "skipped", "reason": "No page provided"}
                filler = FormFiller(self.page)
                return filler.fill_form(form_values=params.get("form_values"), preview=False)

        if module == "email":
            from email_composer import draft_new_email
            from email_sender import send_email
            from final_project.module6_memory.memory_store import get_profile

            profile = get_profile()
            if action == "send":
                draft = draft_new_email(params.get("intent", ""), tone=params.get("tone", "professional"))
                confirmed = await self._confirm_send(draft, params.get("to") or profile.get("email", ""))
                if not confirmed:
                    return {"sent": False, "reason": "confirmation required"}
                return send_email(
                    to=params.get("to") or profile.get("email", ""),
                    subject=draft["subject"],
                    body=draft["body"],
                    confirm=True,
                )

        if module == "calendar":
            from calendar_helper import create_event
            if action == "add_event":
                return create_event(
                    summary=params.get("title", "Task"),
                    start_iso=params.get("start_iso", "2026-07-07T09:00:00+00:00"),
                    end_iso=params.get("end_iso", "2026-07-07T10:00:00+00:00"),
                    description=params.get("description", ""),
                )

        if module == "memory":
            from final_project.module6_memory.memory_store import save_note, search_history, get_profile
            if action == "save_note":
                return {"note_id": save_note(content=params.get("content", ""), title=params.get("title", ""))}
            if action == "search_history":
                return search_history(params.get("query", ""))
            if action == "get_profile":
                return get_profile()

        raise ValueError(f"Unknown module/action: {module}/{action}")

    async def _confirm_send(self, draft: dict, to: str) -> bool:
        print(f"\n📧 Preview for {to}")
        print(f"Subject: {draft['subject']}")
        print(f"Body: {draft['body']}")
        response = input("Send this email? [y/N]: ").strip().lower()
        return response in {"y", "yes"}

    async def _default_on_step(self, step_num, module, description, status, result) -> None:
        icon = {"running": "⏳", "done": "✅", "error": "❌"}.get(status, "•")
        print(f"{icon} Step {step_num} [{module}] {description}")
