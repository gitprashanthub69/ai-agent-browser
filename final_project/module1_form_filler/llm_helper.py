import json
import os
import textwrap
from typing import Any, Dict, Optional

try:
    import google.generativeai as genai
except Exception:
    genai = None


class LLMHelper:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None
        if genai is not None and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception:
                self.model = None

    def generate_text(self, prompt: str) -> str:
        if self.model is None:
            return self._fallback_text(prompt)
        try:
            response = self.model.generate_content(prompt)
            return getattr(response, "text", "") or self._fallback_text(prompt)
        except Exception:
            return self._fallback_text(prompt)

    def _fallback_text(self, prompt: str) -> str:
        return textwrap.shorten(prompt, width=180, placeholder="...")

    def build_long_answer(self, profile: Dict[str, Any], prompt: str) -> str:
        context = json.dumps(profile, indent=2)
        return self.generate_text(f"Using this profile:\n{context}\n\nWrite a polished response for: {prompt}")
