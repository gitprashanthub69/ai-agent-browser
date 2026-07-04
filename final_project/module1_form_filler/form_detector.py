from __future__ import annotations

from typing import Any, Dict, List


class FormDetector:
    def __init__(self, page: Any) -> None:
        self.page = page

    def detect_fields(self) -> List[Dict[str, Any]]:
        script = r"""
        () => {
          const fields = [];
          const selectors = ['input', 'textarea', 'select'];
          document.querySelectorAll(selectors.join(',')).forEach((el) => {
            const type = (el.getAttribute('type') || '').toLowerCase();
            const name = el.getAttribute('name') || el.getAttribute('id') || el.getAttribute('placeholder') || el.tagName.toLowerCase();
            fields.push({
              tag: el.tagName.toLowerCase(),
              type,
              name,
              placeholder: el.getAttribute('placeholder') || '',
              label: (el.labels && el.labels[0] ? el.labels[0].textContent.trim() : '')
            });
          });
          return fields;
        }
        """
        return self.page.evaluate(script) or []
