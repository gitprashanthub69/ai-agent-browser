"""Send emails only after explicit confirmation."""

import base64
from email.mime.text import MIMEText

try:
    from .gmail_auth import get_gmail_service
except ImportError:  # pragma: no cover - allows direct script execution
    from gmail_auth import get_gmail_service


def _build_message(to, subject, body, thread_id=None):
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    payload = {"raw": raw}
    if thread_id:
        payload["threadId"] = thread_id
    return payload


def preview_email(to, subject, body):
    """Show a preview without sending the message."""
    print("=" * 50)
    print("EMAIL PREVIEW (not sent yet)")
    print("=" * 50)
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print("-" * 50)
    print(body)
    print("=" * 50)


def send_email(to, subject, body, confirm=False, thread_id=None):
    """Send a single email only when confirm=True."""
    preview_email(to, subject, body)

    if not confirm:
        print("\n⚠️  NOT SENT — call again with confirm=True to actually send.")
        return {"sent": False, "reason": "confirmation required"}

    service = get_gmail_service()
    message = _build_message(to, subject, body, thread_id=thread_id)
    sent = service.users().messages().send(userId="me", body=message).execute()

    print(f"\n✅ Sent! Message ID: {sent['id']}")
    return {"sent": True, "message_id": sent["id"]}


def reply_to_thread(thread_id, to, subject, body, confirm=False):
    """Send a reply within an existing thread."""
    return send_email(to, subject, body, confirm=confirm, thread_id=thread_id)


def send_group_email(recipients, subject, body, confirm=False):
    """Send the same message to multiple recipients, one by one."""
    print(f"About to send to {len(recipients)} people: {', '.join(recipients)}")
    results = []

    if not confirm:
        preview_email(", ".join(recipients), subject, body)
        print("\n⚠️  NOT SENT — call again with confirm=True to actually send to the group.")
        return {"sent": False, "reason": "confirmation required"}

    for person in recipients:
        result = send_email(person, subject, body, confirm=True)
        results.append({"to": person, **result})

    return {"sent": True, "results": results}


if __name__ == "__main__":
    send_email(
        to="test@example.com",
        subject="Test email",
        body="This is just a preview test.",
    )
