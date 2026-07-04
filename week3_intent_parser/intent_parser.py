"""
intent_parser.py

Provides `parse_intent(command_text: str) -> dict` which uses the Anthropic
API when an API key is available, and otherwise falls back to a small
rule-based parser. The function is defensive and returns structured JSON-like
Python dicts and never raises for ordinary errors (missing API key, bad JSON,
network failures).
"""

from __future__ import annotations
import importlib
import os
import json
import re
from typing import Any, Dict

anthropic = None
try:
    anthropic = importlib.import_module("anthropic")
except Exception:
    anthropic = None  # Not installed; fallback parser will be used

genai = None


ANTHROPIC_ENV = "ANTHROPIC_API_KEY"


class _CompatModel:
    """Provide a tiny model interface compatible with the Week 6 tests."""

    def generate_content(self, prompt: str):
        return None


model = _CompatModel()

FEW_SHOT = """
Example 1:
User: "Open a new tab and go to https://news.ycombinator.com"
Parsed JSON:
{"action": "open_url", "url": "https://news.ycombinator.com", "args": {}}

Example 2:
User: "Search Google for Python asyncio tutorials"
Parsed JSON:
{"action": "search", "engine": "google", "query": "Python asyncio tutorials"}

Example 3:
User: "Email John about the meeting tomorrow at 10am"
Parsed JSON:
{"action": "email", "recipient": "John", "subject": "meeting tomorrow", "time": "10:00"}
"""


def _fallback_parse(text: str) -> Dict[str, Any]:
    """Simple rule-based fallback parser that returns the Week 6 intent schema."""
    t = text.strip()

    if not t:
        return {
            "intent": "unknown",
            "target": None,
            "parameters": {},
            "needs_clarification": False,
            "clarification_question": None,
            "error": "invalid_input",
        }

    lowered = t.lower()

    url_match = re.search(r"https?://\S+", t)
    if url_match:
        return {
            "intent": "navigate",
            "target": url_match.group(0),
            "parameters": {},
            "needs_clarification": False,
            "clarification_question": None,
        }

    if lowered.startswith("search") or "search for" in lowered:
        query = re.sub(r"(?i)search( for)?", "", t).strip(" :")
        return {
            "intent": "navigate",
            "target": query,
            "parameters": {"query": query},
            "needs_clarification": False,
            "clarification_question": None,
        }

    if lowered.startswith("email") or lowered.startswith("send email"):
        m = re.match(r"(?i)email\s+(\S+)(\s+about\s+(.*))?", t)
        recipient = m.group(1) if m else None
        subject = m.group(3) if m and m.group(3) else ""
        return {
            "intent": "email",
            "target": recipient or "current page",
            "parameters": {"subject": subject},
            "needs_clarification": not recipient,
            "clarification_question": "Who should receive this email?" if not recipient else None,
        }

    if lowered.startswith("click"):
        target = t[len("click"):].strip()
        return {
            "intent": "click",
            "target": target or "target element",
            "parameters": {"selector": target},
            "needs_clarification": False,
            "clarification_question": None,
        }

    if lowered.startswith("fill") or "fill" in lowered:
        target = t[len("fill"):].strip() if lowered.startswith("fill") else t
        return {
            "intent": "fill_form",
            "target": target or "form",
            "parameters": {},
            "needs_clarification": False,
            "clarification_question": None,
        }

    if lowered.startswith("summarize") or "summarize" in lowered:
        return {
            "intent": "summarize",
            "target": "current page",
            "parameters": {},
            "needs_clarification": False,
            "clarification_question": None,
        }

    return {
        "intent": "unknown",
        "target": None,
        "parameters": {},
        "needs_clarification": False,
        "clarification_question": None,
        "error": "unsupported_command",
    }


def parse_intent(command_text: str, use_model: bool = True) -> Dict[str, Any]:
    """Parse an English command into a structured intent dict.

    If the environment variable `ANTHROPIC_API_KEY` is present and the
    `anthropic` package is importable, this will call the Anthropic completions
    API with a few-shot prompt and attempt to parse the result as JSON.

    On any failure (missing key, import, timeout, invalid JSON), the function
    returns a best-effort dict produced by `_fallback_parse`.
    """
    if not command_text or not isinstance(command_text, str):
        return {
            "intent": "unknown",
            "target": None,
            "parameters": {},
            "needs_clarification": False,
            "clarification_question": None,
            "error": "invalid_input",
            "message": "Command must be a non-empty string",
        }

    api_key = os.getenv(ANTHROPIC_ENV)
    if use_model:
        try:
            prompt = FEW_SHOT + f"\nUser: \"{command_text}\"\nParsed JSON:\n"

            if api_key and anthropic is not None:
                client = anthropic.Client(api_key=api_key)
                resp = client.completions.create(
                    model="claude-2",
                    prompt=prompt,
                    max_tokens_to_sample=300,
                    temperature=0.0,
                )
                text_out = getattr(resp, "completion", None)
            else:
                resp = model.generate_content(prompt)
                text_out = getattr(resp, "text", None)
                if text_out is None and isinstance(resp, dict):
                    text_out = resp.get("text")

            if text_out:
                json_text_match = re.search(r"\{[\s\S]*\}", text_out)
                if json_text_match:
                    try:
                        parsed = json.loads(json_text_match.group(0))
                        return parsed
                    except Exception:
                        pass
        except Exception:
            pass

    # fallback parser used when model not available or failed
    try:
        return _fallback_parse(command_text)
    except Exception as e:
        return {
            "intent": "unknown",
            "target": None,
            "parameters": {},
            "needs_clarification": False,
            "clarification_question": None,
            "error": "fallback_failed",
            "message": str(e),
        }


if __name__ == "__main__":
    # quick local demo when running the module directly
    examples = [
        "Open a new tab and go to https://news.ycombinator.com",
        "Search Google for Python async tutorials",
        "Email Alice about the report",
    ]
    for ex in examples:
        print("Command:", ex)
        print("Parsed:", parse_intent(ex))
        print()
