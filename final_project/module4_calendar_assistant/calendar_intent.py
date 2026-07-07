"""
calendar_intent.py
Converts plain English like "schedule a call with Raj tomorrow at 3pm for 30 min"
into structured event data, then calls calendar_helper to create it.
"""

import os
import json
import datetime
import google.generativeai as genai
from .calendar_helper import create_event

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def parse_event_request(instruction):
    today = datetime.date.today().isoformat()
    prompt = f"""Today's date is {today}. Convert this instruction into JSON:
"{instruction}"

Return ONLY valid JSON, no markdown, in this exact format:
{{
  "summary": "short event title",
  "start": "YYYY-MM-DDTHH:MM:SS",
  "end": "YYYY-MM-DDTHH:MM:SS",
  "attendees": []
}}
"""
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)


def schedule_from_text(instruction, confirm=False):
    """Parses instruction, previews it, only creates event if confirm=True."""
    event_data = parse_event_request(instruction)

    print("=" * 40)
    print("EVENT PREVIEW")
    print(f"Title: {event_data['summary']}")
    print(f"Start: {event_data['start']}")
    print(f"End:   {event_data['end']}")
    print("=" * 40)

    if not confirm:
        print("⚠️  NOT created — call again with confirm=True to add to calendar.")
        return {"created": False, "preview": event_data}

    result = create_event(
        event_data["summary"], event_data["start"], event_data["end"],
        attendees=event_data.get("attendees") or None
    )
    print(f"✅ Created: {result['link']}")
    return {"created": True, **result}


if __name__ == "__main__":
    schedule_from_text("Schedule a study session tomorrow at 5pm for 1 hour", confirm=False)
