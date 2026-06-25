"""
test_commands.py

Runs 10 sample commands through `parse_intent` and writes the results to
`test_commands.md`. If no Anthropic API key is present the local fallback parser
is used, so this script can be run offline.
"""
from pathlib import Path
import json
from intent_parser import parse_intent

OUTPUT = Path(__file__).resolve().parent / "test_commands.md"

COMMANDS = [
    "Open a new tab and go to https://news.ycombinator.com",
    "Search for best Python web frameworks",
    "Email prashant.sharma@example.com about the meeting tomorrow",
    "Click the Submit button on the form",
    "Fill the name field with John Doe",
    "Open https://playwright.dev and take a screenshot",
    "Search for Playwright Python tutorials",
    "Send email to team@example.com: status update",
    "Click the first result",
    "Fill the address field with 123 Main St",
]


def main():
    results = []
    for cmd in COMMANDS:
        parsed = parse_intent(cmd)
        results.append({"command": cmd, "parsed": parsed})

    # write a markdown report
    lines = ["# Test Commands Results\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. `{r['command']}`\n")
        lines.append("```json\n")
        lines.append(json.dumps(r['parsed'], indent=2, ensure_ascii=False))
        lines.append("\n```\n")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote test results to {OUTPUT}")


if __name__ == "__main__":
    main()
