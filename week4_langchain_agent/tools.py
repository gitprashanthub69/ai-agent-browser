"""
Week 4 — LangChain Tools
3 custom tools that wrap Playwright browser actions:
  - navigate_to(url)
  - click_element(selector)
  - type_text(selector, text)
"""

from langchain.tools import tool

# ── Tool 1: Navigate ──────────────────────────────────────────────────────────

@tool
def navigate_to(url: str) -> str:
    """
    Navigate the browser to a given URL.
    Input: a full URL like https://google.com
    Returns: confirmation message or error
    """
    try:
        # In the real agent, this calls Playwright:
        #   await page.goto(url, wait_until="domcontentloaded")
        # For now we simulate so the agent can run without a live browser.
        if not url.startswith("http"):
            url = "https://" + url
        return f"✅ Navigated to {url}"
    except Exception as e:
        return f"❌ Failed to navigate to {url}: {str(e)}"


# ── Tool 2: Click Element ─────────────────────────────────────────────────────

@tool
def click_element(selector: str) -> str:
    """
    Click an element on the current page using a CSS selector.
    Input: CSS selector string like 'button[type=submit]' or '#login-btn'
    Returns: confirmation message or error
    """
    try:
        # Real implementation:
        #   await page.wait_for_selector(selector, timeout=5000)
        #   await page.click(selector)
        return f"✅ Clicked element: {selector}"
    except Exception as e:
        return f"❌ Could not click '{selector}': {str(e)}"


# ── Tool 3: Type Text ─────────────────────────────────────────────────────────

@tool
def type_text(input_str: str) -> str:
    """
    Type text into an input field on the current page.
    Input format: 'selector|||text'  (three pipe characters as separator)
    Example: '#email|||hello@example.com'
    Returns: confirmation message or error
    """
    try:
        if "|||" not in input_str:
            return "❌ Input must be in format: selector|||text"
        selector, text = input_str.split("|||", 1)
        selector = selector.strip()
        text = text.strip()
        # Real implementation:
        #   await page.wait_for_selector(selector, timeout=5000)
        #   await page.fill(selector, text)
        return f"✅ Typed '{text}' into {selector}"
    except Exception as e:
        return f"❌ Failed to type text: {str(e)}"


# Export all tools as a list for the agent
TOOLS = [navigate_to, click_element, type_text]
