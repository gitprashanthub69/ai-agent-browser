import json
from pathlib import Path
from typing import Any, Dict, Optional

PROFILE_PATH = Path(__file__).resolve().parent / "profile.json"


class ProfileStore:
    def __init__(self, path: Optional[str] = None) -> None:
        self.path = Path(path or PROFILE_PATH)
        self._ensure_exists()

    def _ensure_exists(self) -> None:
        if not self.path.exists():
            self.path.write_text(
                json.dumps(
                    {
                        "name": "",
                        "email": "",
                        "phone": "",
                        "college": "",
                        "skills": [],
                        "resume_path": "",
                        "linkedin": "",
                        "portfolio": "",
                        "bio": "",
                        "sop": "",
                        "github": "",
                        "address": "",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

    def load(self) -> Dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: Dict[str, Any]) -> None:
        current = self.load()
        current.update(data)
        self.path.write_text(json.dumps(current, indent=2), encoding="utf-8")

    def get(self, key: str, default: Any = None) -> Any:
        return self.load().get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.save({key: value})

    def update_from_form(self, form_values: Dict[str, Any]) -> None:
        self.save(form_values)
