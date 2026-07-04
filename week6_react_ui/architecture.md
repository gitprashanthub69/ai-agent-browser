# AI Browser Agent — Architecture Document

## System Overview

A full-stack agentic AI assistant that converts plain-English commands into real browser actions.
The user types a command → the agent reasons, plans, and executes it step by step → results stream back live.

---

## Architecture Diagram

```text
User Interface (React) → FastAPI Backend → Agent Executor → Browser Layer → External APIs
```

- React UI handles command entry, live activity logs, and profile management.
- FastAPI exposes command submission, task status, and profile endpoints.
- The agent executor uses the intent parser and browser tools to complete tasks.
- Playwright performs navigation, clicks, typing, and screenshots.
- Optional external services include Gmail and PDF parsing.

---

## Week 6 Focus

- Build the React dashboard with a polished violet/black UI.
- Connect the UI to FastAPI command and profile endpoints.
- Stream task steps into the activity log.
- Keep the intent parser tests reproducible and lightweight.
