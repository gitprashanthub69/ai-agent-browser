"""Draft emails with Gemini without sending them."""

import os

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None


if genai is not None and os.environ.get("GEMINI_API_KEY"):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    _model = genai.GenerativeModel("gemini-1.5-flash")
else:
    _model = None


def draft_new_email(instruction, tone="professional"):
    """Draft a new email from a plain-English instruction."""
    if _model is None:
        return {
            "subject": "Draft unavailable",
            "body": "Set GEMINI_API_KEY to enable AI drafting.",
        }

    prompt = f"""Write an email based on this instruction: \"{instruction}\"

Tone: {tone}
Return your answer in EXACTLY this format (no extra text):
SUBJECT: <subject line>
BODY:
<email body>
"""
    response = _model.generate_content(prompt)
    return _parse_subject_body(response.text)


def draft_reply(thread_messages, instruction, tone="professional"):
    """Draft a reply for an existing thread."""
    if _model is None:
        return {
            "subject": "Reply draft unavailable",
            "body": "Set GEMINI_API_KEY to enable AI drafting.",
        }

    context = "\n\n---\n\n".join(
        f"From: {m['from']}\n{m['body'][:1000]}" for m in thread_messages
    )

    prompt = f"""Here is an email thread:

{context}

Write a reply based on this instruction: \"{instruction}\"
Tone: {tone}
Return your answer in EXACTLY this format (no extra text):
SUBJECT: <subject line, usually \"Re: ...\" >
BODY:
<email body>
"""
    response = _model.generate_content(prompt)
    return _parse_subject_body(response.text)


def _parse_subject_body(text):
    subject = ""
    body_lines = []
    in_body = False

    for line in text.splitlines():
        if line.strip().upper().startswith("SUBJECT:"):
            subject = line.split(":", 1)[1].strip()
        elif line.strip().upper().startswith("BODY:"):
            in_body = True
        elif in_body:
            body_lines.append(line)

    return {
        "subject": subject or "(no subject)",
        "body": "\n".join(body_lines).strip(),
    }


if __name__ == "__main__":
    draft = draft_new_email(
        "email my manager Priya letting her know I'll be 20 minutes late to the 10am standup"
    )
    print("SUBJECT:", draft["subject"])
    print("BODY:\n", draft["body"])
