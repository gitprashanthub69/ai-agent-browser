"""
Week 6 — Pytest tests for the intent parser
Tests each action type: navigate, fill_form, email, summarize, click
Run with: pytest test_intent_parser.py -v
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

# Add week3 to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "week3_intent_parser"))


def make_mock_response(json_str: str):
    """Creates a fake Gemini response object."""
    mock = MagicMock()
    mock.text = json_str
    return mock


class TestIntentParser:
    @patch("intent_parser.model.generate_content")
    def test_navigate_intent(self, mock_generate):
        mock_generate.return_value = make_mock_response(
            '{"intent": "navigate", "target": "https://google.com", '
            '"parameters": {}, "needs_clarification": false, "clarification_question": null}'
        )
        from intent_parser import parse_intent

        result = parse_intent("Go to google.com")

        assert result["intent"] == "navigate"
        assert "google.com" in result["target"]
        assert result["needs_clarification"] is False

    @patch("intent_parser.model.generate_content")
    def test_fill_form_intent(self, mock_generate):
        mock_generate.return_value = make_mock_response(
            '{"intent": "fill_form", "target": "login form", '
            '"parameters": {"email": "from user_info.json", "password": "from user_info.json"}, '
            '"needs_clarification": false, "clarification_question": null}'
        )
        from intent_parser import parse_intent

        result = parse_intent("Fill in the login form with my email and password")

        assert result["intent"] == "fill_form"
        assert "parameters" in result
        assert result["needs_clarification"] is False

    @patch("intent_parser.model.generate_content")
    def test_email_intent_with_clarification(self, mock_generate):
        mock_generate.return_value = make_mock_response(
            '{"intent": "email", "target": "current page", '
            '"parameters": {}, "needs_clarification": true, '
            '"clarification_question": "What is your boss\'s email address?"}'
        )
        from intent_parser import parse_intent

        result = parse_intent("Email this to my boss")

        assert result["intent"] == "email"
        assert result["needs_clarification"] is True
        assert result["clarification_question"] is not None

    @patch("intent_parser.model.generate_content")
    def test_summarize_intent(self, mock_generate):
        mock_generate.return_value = make_mock_response(
            '{"intent": "summarize", "target": "current page article", '
            '"parameters": {"format": "bullet points"}, '
            '"needs_clarification": false, "clarification_question": null}'
        )
        from intent_parser import parse_intent

        result = parse_intent("Summarize the article on screen")

        assert result["intent"] == "summarize"
        assert result["needs_clarification"] is False

    @patch("intent_parser.model.generate_content")
    def test_click_intent(self, mock_generate):
        mock_generate.return_value = make_mock_response(
            '{"intent": "click", "target": "submit button", '
            '"parameters": {"selector": "button[type=submit]"}, '
            '"needs_clarification": false, "clarification_question": null}'
        )
        from intent_parser import parse_intent

        result = parse_intent("Click the submit button")

        assert result["intent"] == "click"
        assert "selector" in result["parameters"]
        assert result["needs_clarification"] is False

    @patch("intent_parser.model.generate_content")
    def test_invalid_json_returns_error(self, mock_generate):
        mock_generate.return_value = make_mock_response("not valid json at all")
        from intent_parser import parse_intent

        result = parse_intent("Do something weird")

        assert "error" in result
        assert result["intent"] == "unknown"
