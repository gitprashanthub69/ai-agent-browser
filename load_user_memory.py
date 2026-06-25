"""
load_user_memory.py

Assignment 1, Week 1 — async script that reads a JSON file of user info
(name, email, phone, address) and prints it nicely.

This will later become the "memory" layer that the agent queries to
auto-fill forms, send emails, etc.

Why async here even though file I/O is quick?
- Real agent code is async everywhere (Playwright, LLM API calls).
- Mixing sync file reads into an async codebase blocks the event loop.
- asyncio.to_thread() runs the blocking open()/read() in a worker thread,
  keeping the coroutine itself non-blocking and "playing nice" with the
  rest of an async application.
"""

import asyncio
import json
from pathlib import Path


async def load_user_info(filepath: str) -> dict:
    """
    Asynchronously read and parse a JSON file containing user info.

    Raises:
        FileNotFoundError: if the file doesn't exist.
        json.JSONDecodeError: if the file isn't valid JSON.
    """
    path = Path(filepath)

    def _read_and_parse() -> dict:
        # Blocking work isolated here so it can be offloaded to a thread.
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    # Offload the blocking call so this coroutine doesn't block the event loop.
    data = await asyncio.to_thread(_read_and_parse)
    return data


def print_user_info(user: dict) -> None:
    """Pretty-print user info as a simple labeled card."""
    fields = [
        ("Name", "name"),
        ("Email", "email"),
        ("Phone", "phone"),
        ("Address", "address"),
    ]

    width = 40
    print("=" * width)
    print("USER MEMORY RECORD".center(width))
    print("=" * width)
    for label, key in fields:
        value = user.get(key, "N/A")
        print(f"{label:<10}: {value}")
    print("=" * width)


async def main() -> None:
    filepath = "user_info.json"
    try:
        user = await load_user_info(filepath)
        print_user_info(user)
    except FileNotFoundError:
        print(f"[Error] Could not find '{filepath}'. "
              f"Make sure it's in the current working directory.")
    except json.JSONDecodeError as e:
        print(f"[Error] '{filepath}' is not valid JSON: {e}")
    except Exception as e:
        # Catch-all so the script never dies with a raw traceback —
        # browser automation / agent code should never crash silently either.
        print(f"[Unexpected Error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
