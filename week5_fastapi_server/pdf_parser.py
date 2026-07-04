"""
Week 5 — PDF Parser
Extracts text from uploaded resume PDFs.
The agent uses this text to auto-fill job application forms.
"""

import os


def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extracts all text from a PDF file.
    Returns {"success": True, "text": "..."} or {"success": False, "error": "..."}
    """
    if not os.path.exists(pdf_path):
        return {"success": False, "error": f"File not found: {pdf_path}"}

    try:
        import pypdf
        text = ""
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""

        text = text.strip()
        if not text:
            return {"success": False, "error": "PDF appears to be scanned/image-based — no text extracted."}

        return {"success": True, "text": text, "pages": len(reader.pages)}

    except ImportError:
        return {"success": False, "error": "pypdf not installed. Run: pip install pypdf"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_key_fields(text: str) -> dict:
    """
    Very simple field extractor from resume text.
    Returns a dict of likely name/email/phone/skills.
    """
    import re

    fields = {}

    # Email
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        fields["email"] = email_match.group()

    # Phone (Indian and international formats)
    phone_match = re.search(r"(\+?\d[\d\s\-().]{8,14}\d)", text)
    if phone_match:
        fields["phone"] = phone_match.group().strip()

    # Skills (look for a "Skills" section)
    skills_match = re.search(r"(?i)skills[:\s]+(.*?)(?:\n\n|\Z)", text, re.DOTALL)
    if skills_match:
        fields["skills"] = skills_match.group(1).strip()[:300]

    return fields


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pdf_parser.py resume.pdf")
    else:
        result = extract_text_from_pdf(sys.argv[1])
        if result["success"]:
            print(f"Pages: {result['pages']}")
            print(f"Text preview:\n{result['text'][:500]}...")
            print(f"\nExtracted fields: {extract_key_fields(result['text'])}")
        else:
            print(f"Error: {result['error']}")
