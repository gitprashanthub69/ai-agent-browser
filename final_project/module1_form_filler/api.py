from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from profile_store import ProfileStore
from form_filler import FormFiller

app = FastAPI(title="Module 1 Form Filler")


class ProfilePayload(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    college: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None
    bio: Optional[str] = None
    sop: Optional[str] = None


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "module": "module1_form_filler"}


@app.get("/form/profile")
def get_profile() -> Dict[str, Any]:
    return ProfileStore().load()


@app.post("/form/profile")
def save_profile(payload: ProfilePayload) -> Dict[str, Any]:
    store = ProfileStore()
    data = {k: v for k, v in payload.dict().items() if v is not None}
    store.save(data)
    return store.load()


@app.post("/form/fill")
def fill_form(url: str) -> Dict[str, Any]:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        result = FormFiller(page).fill_form()
        browser.close()
        return result
