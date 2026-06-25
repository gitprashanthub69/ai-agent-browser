"""
script1_navigator.py

Week 2, Assignment 2 - Script 1: Navigator

Opens Hacker News, extracts the titles of the top 5 articles,
and saves them to a JSON file.

Run:
    python script1_navigator.py
"""

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "top_articles.json"
NUM_ARTICLES = 5
URL = "https://news.ycombinator.com/"


async def get_top_articles() -> list[dict]:
    """Launch a browser, open Hacker News, and scrape the top N article titles."""
    articles = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(URL, timeout=15000, wait_until="domcontentloaded")
        except PlaywrightTimeoutError:
            print(f"[Error] Timed out loading {URL}")
            await browser.close()
            return articles

        try:
            await page.wait_for_selector(".titleline", timeout=10000)
            title_locators = page.locator(".titleline > a")
            count = await title_locators.count()

            if count == 0:
                print("[Error] No article titles found on the page (selector may be outdated).")
                await browser.close()
                return articles

            for i in range(min(NUM_ARTICLES, count)):
                title_text = await title_locators.nth(i).inner_text()
                link_href = await title_locators.nth(i).get_attribute("href")
                articles.append({
                    "rank": i + 1,
                    "title": title_text,
                    "url": link_href,
                })

        except PlaywrightTimeoutError:
            print("[Error] Timed out waiting for article titles to appear.")
        finally:
            await browser.close()

    return articles


def save_to_json(data: list[dict], filepath: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} articles to {filepath}")


async def main():
    articles = await get_top_articles()
    if articles:
        for a in articles:
            print(f"{a['rank']}. {a['title']}")
        save_to_json(articles, OUTPUT_FILE)
    else:
        print("No articles were extracted — nothing saved.")


if __name__ == "__main__":
    asyncio.run(main())
