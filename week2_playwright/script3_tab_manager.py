"""
script3_tab_manager.py

Week 2, Assignment 2 - Script 3: Tab Manager

Opens 5 tabs in parallel (one browser, 5 pages/tabs), captures each
page's title, then closes all tabs except the first.

Run:
    python script3_tab_manager.py
"""

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "tab_titles.json"
URLS = [
    "https://news.ycombinator.com/",
    "https://www.bbc.com/news",
    "https://www.python.org/",
    "https://playwright.dev/",
    "https://github.com/",
]


async def open_and_get_title(browser, url: str) -> dict:
    """Open one URL in a new tab/page and return its title (or an error note)."""
    page = await browser.new_page()
    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        title = await page.title()
        return {"url": url, "title": title, "page": page, "error": None}
    except PlaywrightTimeoutError:
        return {"url": url, "title": None, "page": page, "error": "timeout loading page"}
    except Exception as e:
        return {"url": url, "title": None, "page": page, "error": f"{type(e).__name__}: {e}"}


async def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        tasks = [open_and_get_title(browser, url) for url in URLS]
        tab_results = await asyncio.gather(*tasks)

        for r in tab_results:
            status = r["title"] if r["title"] else f"FAILED ({r['error']})"
            print(f"{r['url']} -> {status}")
            results.append({"url": r["url"], "title": r["title"], "error": r["error"]})

        first_page = tab_results[0]["page"]
        for r in tab_results[1:]:
            await r["page"].close()
        print(f"\nClosed {len(tab_results) - 1} tabs. Kept open: {tab_results[0]['url']}")

        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Saved titles to {OUTPUT_FILE}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
