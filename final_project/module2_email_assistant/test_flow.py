"""Run the Module 2 email assistant flow and write proof output."""

from pathlib import Path

try:
    from .email_composer import draft_new_email
    from .email_reader import list_recent_emails, summarize_thread
except ImportError:  # pragma: no cover - allows direct script execution
    from email_composer import draft_new_email
    from email_reader import list_recent_emails, summarize_thread

output_lines = ["# Module 2 - Email Assistant - Test Run\n"]

print("Step 1: Listing recent emails...")
try:
    emails = list_recent_emails(max_results=3)
    output_lines.append("## Recent Emails\n")
    for email in emails:
        line = f"- **{email['subject']}** (from: {email['from']})"
        print(line)
        output_lines.append(line)

    if emails:
        print("\nStep 2: Summarizing first thread...")
        summary = summarize_thread(emails[0]["thread_id"])
        print(summary)
        output_lines.append("\n## Thread Summary\n")
        output_lines.append(summary)
except Exception as exc:  # pragma: no cover - depends on local credentials
    output_lines.append("## Recent Emails\n")
    output_lines.append(f"Gmail access was not available: {exc}\n")
    print(f"Gmail access was not available: {exc}")

print("\nStep 3: Drafting a test email...")
draft = draft_new_email("email my professor to say thanks for the extension")
print("SUBJECT:", draft["subject"])
print("BODY:", draft["body"])
output_lines.append("\n## Drafted Email\n")
output_lines.append(f"**Subject:** {draft['subject']}\n")
output_lines.append(f"**Body:**\n\n{draft['body']}")

output_lines.append(
    "\n\n## Note\nSending was NOT tested here on purpose — "
    "sending always requires confirm=True and is tested manually."
)

proof_path = Path(__file__).resolve().parent / "email_assistant_proof.md"
proof_path.write_text("\n".join(output_lines), encoding="utf-8")

print(f"\n✅ Done. Wrote {proof_path.name}")
