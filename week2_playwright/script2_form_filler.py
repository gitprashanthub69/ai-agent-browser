"""
script2_form_filler.py

Week 2, Assignment 2 - Script 2: Form Filler

Goes to demoqa.com/automation-practice-form, fills every field from a
JSON file, screenshots the filled (but unsubmitted) form, then submits.

Run:
    python script2_form_filler.py
"""

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "form_data.json"
OUTPUT_DIR = BASE_DIR / "output"
SCREENSHOT_FILE = OUTPUT_DIR / "form_before_submit.png"
URL = "https://demoqa.com/automation-practice-form"


def load_form_data(filepath: Path) -> dict:
    with filepath.open("r", encoding="utf-8") as f:
        return json.load(f)


async def fill_form(page, data: dict) -> None:
    """Fill each field on the demoqa practice form using the JSON data."""
    await page.fill("#firstName", data["firstName"])
    await page.fill("#lastName", data["lastName"])
    await page.fill("#userEmail", data["email"])

    gender = data["gender"].strip().lower()
    if gender == "male":
        await page.click("label[for='gender-radio-1']")
    elif gender == "female":
        await page.click("label[for='gender-radio-2']")
    else:
        gender_label = page.locator("label", has_text=data["gender"], exact=True)
        await gender_label.first.click()

    await page.fill("#userNumber", data["mobile"])
    await page.fill("#currentAddress", data["currentAddress"])

    await page.click("#state")
    await page.click(f"text={data['state']}")

    await page.click("#city")
    await page.click(f"text={data['city']}")


async def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_form_data(DATA_FILE)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(URL, timeout=15000, wait_until="domcontentloaded")
        except PlaywrightTimeoutError:
            print(f"[Error] Timed out loading {URL}")
            await browser.close()
            return

        try:
            await page.evaluate("""
                document.querySelectorAll('#fixedban, .ad, iframe').forEach(el => el.remove());
            """)

            await page.wait_for_selector("#firstName", timeout=10000)
            await fill_form(page, data)

            await page.screenshot(path=SCREENSHOT_FILE)
            print(f"Screenshot saved to {SCREENSHOT_FILE}")

            await page.click("#submit")
            await page.wait_for_selector(".modal-content", timeout=5000)
            print("Form submitted successfully - confirmation modal appeared.")

        except PlaywrightTimeoutError as e:
            print(f"[Error] A required element did not appear in time: {e}")
        except Exception as e:
            print(f"[Unexpected Error] {type(e).__name__}: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
