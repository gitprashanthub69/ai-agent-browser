"""Vision helper for Module 3.

Uses Playwright to capture a browser screenshot and Gemini Vision to describe the page
or find requested UI elements.
"""

import os
from typing import Optional

from playwright.sync_api import sync_playwright

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None


if genai is not None and os.environ.get("GEMINI_API_KEY"):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    _model = genai.GenerativeModel("gemini-1.5-flash")
else:
    _model = None


def describe_page(url: str, instruction: Optional[str] = None) -> dict:
    """Open a page, capture a screenshot, and ask Gemini Vision to describe it."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)
        browser.close()

    if _model is None:
        return {
            "url": url,
            "description": "Gemini Vision is unavailable. Set GEMINI_API_KEY to enable image analysis.",
            "screenshot": screenshot_path,
        }

    prompt = (
        "Describe this webpage and its main interactive elements. "
        "Focus on what a user would need to know first."
    )
    if instruction:
        prompt = f"{prompt}\nAdditional instruction: {instruction}"

    with open(screenshot_path, "rb") as handle:
        image_bytes = handle.read()

    response = _model.generate_content(
        [prompt, {"mime_type": "image/png", "data": image_bytes}],
        request_options={"timeout": 60000},
    )

    return {
        "url": url,
        "description": response.text.strip(),
        "screenshot": screenshot_path,
    }


def find_element(url: str, query: str) -> dict:
    """Describe the element matching a natural-language query."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)
        browser.close()

    if _model is None:
        return {
            "url": url,
            "query": query,
            "result": "Gemini Vision is unavailable. Set GEMINI_API_KEY to enable image analysis.",
            "screenshot": screenshot_path,
        }

    with open(screenshot_path, "rb") as handle:
        image_bytes = handle.read()

    prompt = f"Look at this webpage and identify the UI element that best matches this request: {query}. Describe it briefly and say where it appears."
    response = _model.generate_content(
        [prompt, {"mime_type": "image/png", "data": image_bytes}],
        request_options={"timeout": 60000},
    )

    return {
        "url": url,
        "query": query,
        "result": response.text.strip(),
        "screenshot": screenshot_path,
    }


if __name__ == "__main__":
    result = describe_page("https://example.com")
    print(result["description"])
    print(f"Screenshot saved to: {result['screenshot']}")
