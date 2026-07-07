"""Parse a natural-language multi-step command into ordered module actions."""

import json
import os
from typing import Optional

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None

if genai is not None and os.environ.get("GEMINI_API_KEY"):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    _model = genai.GenerativeModel("gemini-1.5-flash")
else:
    _model = None

MODULE_SCHEMA = {
    "form": ["fill", "detect_fields", "preview"],
    "email": ["send", "reply", "summarise", "read_inbox"],
    "calendar": ["add_event", "find_free_slot", "get_agenda", "add_recurring"],
    "memory": ["save_note", "search_history", "get_profile"],
    "summary": ["summarise_page", "summarise_url", "compare_pages"],
}

SYSTEM_PROMPT = f"""You are a command parser for an AI browser assistant.
Break the user's command into ordered steps, each assigned to one module.

Available modules and actions:
{json.dumps(MODULE_SCHEMA, indent=2)}

Return ONLY a valid JSON array of steps in this shape:
[
  {{
    "step": 1,
    "module": "module_name",
    "action": "action_name",
    "description": "what this step does",
    "params": {{"key": "value"}},
    "depends_on": null
  }}
]

Rules:
- Keep steps in logical execution order.
- If a step depends on previous output, set depends_on to the earlier step number.
- If unsure, return a simple safe plan.
"""


def parse_command(command: str, context: Optional[dict] = None) -> list[dict]:
    """Return a list of steps for a cross-module command."""
    if not command or not command.strip():
        return []

    context_str = f"\nCurrent context: {json.dumps(context)}" if context else ""
    if _model is None:
        return _fallback_steps(command)

    try:
        response = _model.generate_content(SYSTEM_PROMPT + f"\n\nUser command: \"{command}\"{context_str}")
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        steps = json.loads(raw)
        if isinstance(steps, list) and steps:
            return steps
    except Exception:
        pass

    return _fallback_steps(command)


def _fallback_steps(command: str) -> list[dict]:
    lowered = command.lower()
    steps = []
    if any(word in lowered for word in ["apply", "form", "fill", "submit"]):
        steps.append({
            "step": 1,
            "module": "form",
            "action": "fill",
            "description": "Fill the relevant form fields",
            "params": {"intent": command},
            "depends_on": None,
        })
    if any(word in lowered for word in ["calendar", "deadline", "schedule", "event"]):
        steps.append({
            "step": len(steps) + 1,
            "module": "calendar",
            "action": "add_event",
            "description": "Create a calendar event from the command details",
            "params": {"title": "Scheduled task", "description": command},
            "depends_on": 1 if steps else None,
        })
    if any(word in lowered for word in ["email", "mail", "mentor", "send"]):
        steps.append({
            "step": len(steps) + 1,
            "module": "email",
            "action": "send",
            "description": "Draft and confirm an email before sending",
            "params": {"intent": command},
            "depends_on": 1 if steps else None,
        })
    if not steps:
        steps.append({
            "step": 1,
            "module": "memory",
            "action": "save_note",
            "description": "Record the request in memory",
            "params": {"content": command},
            "depends_on": None,
        })
    return steps


def is_cross_module(command: str) -> bool:
    """Quick heuristic for whether the command spans more than one module."""
    lowered = command.lower()
    module_keywords = {
        "form": ["form", "apply", "submit", "fill"],
        "email": ["email", "mail", "send", "mentor"],
        "calendar": ["calendar", "deadline", "event", "schedule"],
        "memory": ["note", "remember", "save"],
        "summary": ["summarise", "summarize", "summary", "tldr"],
    }
    matches = [name for name, words in module_keywords.items() if any(word in lowered for word in words)]
    return len(matches) >= 2
