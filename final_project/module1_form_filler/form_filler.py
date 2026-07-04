from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Optional

from profile_store import ProfileStore
from form_detector import FormDetector


class FormFiller:
    def __init__(self, page: Any, profile_store: Optional[ProfileStore] = None) -> None:
        self.page = page
        self.profile_store = profile_store or ProfileStore()

    def _map_value(self, field: Dict[str, Any], profile: Dict[str, Any]) -> Optional[str]:
        candidates = []
        raw_name = (field.get("name") or "").lower()
        placeholder = (field.get("placeholder") or "").lower()
        label = (field.get("label") or "").lower()

        for text in [raw_name, placeholder, label]:
            tokens = [token for token in text.replace("/", " ").replace("-", " ").split() if token]
            if not tokens:
                continue
            for token in tokens:
                candidates.append(token)

        synonyms = {
            "name": ["name", "full", "fullname", "your", "first", "last"],
            "email": ["email", "mail"],
            "phone": ["phone", "mobile", "contact"],
            "college": ["college", "university", "school", "institute"],
            "linkedin": ["linkedin"],
            "portfolio": ["portfolio", "website", "site"],
            "github": ["github"],
            "address": ["address", "location", "city"],
            "bio": ["bio", "about", "summary"],
            "sop": ["sop", "statement", "purpose"],
        }

        for key, values in synonyms.items():
            if key in profile and profile[key]:
                if any(token in values for token in candidates):
                    return str(profile[key])

        for key in ["name", "email", "phone", "college", "linkedin", "portfolio", "github", "address", "bio", "sop"]:
            if profile.get(key):
                if any(token in candidates for token in [key] + synonyms.get(key, [])):
                    return str(profile[key])

        return None

    def _upload_resume_if_needed(self, field: Dict[str, Any], profile: Dict[str, Any]) -> bool:
        if field.get("type") not in {"file", "upload"}:
            return False
        resume_path = profile.get("resume_path")
        if not resume_path:
            return False
        path = Path(resume_path)
        if not path.exists():
            return False
        selector = f"input[type='file']"
        self.page.locator(selector).first.set_input_files(str(path))
        return True

    def _preview_and_confirm(self, planned: list[dict[str, Any]]) -> bool:
        print("\nPreview of planned changes:")
        for item in planned:
            print(f"- {item['field']}: {item['value']}")
        answer = input("Approve these changes? [y/N]: ").strip().lower()
        return answer in {"y", "yes"}

    def fill_form(self, form_values: Optional[Dict[str, Any]] = None, preview: bool = True) -> Dict[str, Any]:
        profile = self.profile_store.load()
        detector = FormDetector(self.page)
        fields = detector.detect_fields()

        if form_values:
            profile.update(form_values)
            self.profile_store.save(profile)

        planned: list[dict[str, Any]] = []
        for field in fields:
            if not field.get("name"):
                continue
            if self._upload_resume_if_needed(field, profile):
                planned.append({"field": field.get("name"), "value": "<resume upload>"})
                continue

            value = self._map_value(field, profile)
            if not value:
                continue
            selector = (
                f"input[name=\"{field['name']}\"], "
                f"textarea[name=\"{field['name']}\"], "
                f"select[name=\"{field['name']}\"], "
                f"input[id=\"{field['name']}\"], "
                f"textarea[id=\"{field['name']}\"], "
                f"select[id=\"{field['name']}\"], "
                f"input[type=\"{field.get('type') or 'text'}\"]"
            )
            self.page.locator(selector).first.fill(str(value))
            planned.append({"field": field.get("name"), "value": value})

        if preview and planned and not self._preview_and_confirm(planned):
            return {"fields_detected": len(fields), "filled": [], "preview_cancelled": True, "profile": profile}

        return {"fields_detected": len(fields), "filled": planned, "preview_cancelled": False, "profile": profile}


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill forms using the saved profile")
    parser.add_argument("url", nargs="?", default="https://demoqa.com/automation-practice-form")
    parser.add_argument("--no-preview", action="store_true", help="Skip the approval preview")
    args = parser.parse_args()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(args.url)
        filler = FormFiller(page)
        result = filler.fill_form(preview=not args.no_preview)
        print("Filled fields:", result["filled"])
        browser.close()


if __name__ == "__main__":
    main()
