"""Read and summarize Gmail messages for Module 2."""

import base64
import os

try:
    from .gmail_auth import get_gmail_service
except ImportError:  # pragma: no cover - allows direct script execution
    from gmail_auth import get_gmail_service

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None


if genai is not None and os.environ.get("GEMINI_API_KEY"):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    _model = genai.GenerativeModel("gemini-1.5-flash")
else:
    _model = None


def _get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def _extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            if "parts" in part:
                result = _extract_body(part)
                if result:
                    return result
    else:
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    return ""


def list_recent_emails(max_results=10, query=""):
    """Return a list of recent emails with metadata."""
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me", maxResults=max_results, q=query
    ).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        full = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = full["payload"]["headers"]
        emails.append(
            {
                "id": msg["id"],
                "thread_id": full.get("threadId", ""),
                "subject": _get_header(headers, "Subject"),
                "from": _get_header(headers, "From"),
                "date": _get_header(headers, "Date"),
                "snippet": full.get("snippet", ""),
            }
        )
    return emails


def get_thread(thread_id):
    """Return all messages in a thread with body text."""
    service = get_gmail_service()
    thread = service.users().threads().get(userId="me", id=thread_id).execute()

    messages = []
    for msg in thread["messages"]:
        headers = msg["payload"]["headers"]
        messages.append(
            {
                "id": msg["id"],
                "from": _get_header(headers, "From"),
                "subject": _get_header(headers, "Subject"),
                "date": _get_header(headers, "Date"),
                "body": _extract_body(msg["payload"]),
            }
        )
    return messages


def summarize_thread(thread_id):
    """Use Gemini to summarize a thread, or return a fallback message if unavailable."""
    messages = get_thread(thread_id)

    conversation_text = "\n\n---\n\n".join(
        f"From: {m['from']}\nDate: {m['date']}\n{m['body'][:1500]}" for m in messages
    )

    if _model is None:
        return "Gemini summary unavailable. Set GEMINI_API_KEY to enable AI summaries."

    prompt = f"""Summarize this email thread in 3-5 short sentences.
Mention who is involved, what they want, and any action needed from me.

EMAIL THREAD:
{conversation_text}
"""
    response = _model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    print("Fetching recent emails...\n")
    emails = list_recent_emails(max_results=5)
    for email in emails:
        print(f"- {email['subject']}  (from: {email['from']})")
