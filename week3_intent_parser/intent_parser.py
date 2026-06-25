"""
intent_parser.py

Provides `parse_intent(command_text: str) -> dict` which uses the Anthropic
API when an API key is available, and otherwise falls back to a small
rule-based parser. The function is defensive and returns structured JSON-like
Python dicts and never raises for ordinary errors (missing API key, bad JSON,
network failures).
"""

from __future__ import annotations
import os
import json
import re
from typing import Any, Dict

try:
    import anthropic
except Exception:
    anthropic = None  # Not installed; fallback parser will be used


ANTHROPIC_ENV = "ANTHROPIC_API_KEY"

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
    """Simple rule-based fallback parser if Anthropic isn't available.

    Returns a dict with keys: `action`, and other action-specific fields.
    """
    t = text.strip()

    # url
    url_match = re.search(r"https?://\S+", t)
    if url_match:
        return {"action": "open_url", "url": url_match.group(0), "args": {}}

    # search
    if t.lower().startswith("search") or "search for" in t.lower():
        # crude extraction
        q = re.sub(r"(?i)search( for)?", "", t).strip(" :")
        return {"action": "search", "engine": "google", "query": q}

    # email
    if t.lower().startswith("email") or t.lower().startswith("send email"):
        m = re.match(r"(?i)email\s+(\S+)(\s+about\s+(.*))?", t)
        recipient = m.group(1) if m else None
        subject = m.group(3) if m and m.group(3) else ""
        return {"action": "email", "recipient": recipient, "subject": subject}

    # click / fill
    if t.lower().startswith("click"):
        target = t[len("click"):].strip()
        return {"action": "click", "target": target}

    if t.lower().startswith("fill"):
        target = t[len("fill"):].strip()
        return {"action": "fill", "target": target}

    # default: return as a generic command
    return {"action": "unknown", "text": t}


def parse_intent(command_text: str, use_model: bool = True) -> Dict[str, Any]:
    """Parse an English command into a structured intent dict.

    If the environment variable `ANTHROPIC_API_KEY` is present and the
    `anthropic` package is importable, this will call the Anthropic completions
    API with a few-shot prompt and attempt to parse the result as JSON.

    On any failure (missing key, import, timeout, invalid JSON), the function
    returns a best-effort dict produced by `_fallback_parse`.
    """
    if not command_text or not isinstance(command_text, str):
        return {"action": "error", "error": "invalid_input", "message": "Command must be a non-empty string"}

    api_key = os.getenv(ANTHROPIC_ENV)
    if use_model and api_key and anthropic is not None:
        try:
            client = anthropic.Client(api_key=api_key)
            prompt = FEW_SHOT + f"\nUser: \"{command_text}\"\nParsed JSON:\n"

            # Use a conservative timeout; model output is expected to be JSON text
            resp = client.completions.create(
                model="claude-2",  # user can change model if needed
                prompt=prompt,
                max_tokens_to_sample=300,
                temperature=0.0,
            )

            text_out = resp.completion
            # Attempt to find a JSON block in the output
            json_text_match = re.search(r"\{[\s\S]*\}", text_out)
            if json_text_match:
                try:
                    parsed = json.loads(json_text_match.group(0))
                    return parsed
                except Exception:
                    # fall through to fallback
                    pass
            # If we get here, model output wasn't valid JSON
        except Exception:
            # Any error (network, API, timeout) -> fallback
            pass

    # fallback parser used when model not available or failed
    try:
        return _fallback_parse(command_text)
    except Exception as e:
        return {"action": "error", "error": "fallback_failed", "message": str(e)}


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
