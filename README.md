# 🤖 AI Browser Agent — Full-Stack Agentic AI Assistant

<div align="center">

**An intelligent, agentic AI browser assistant that converts natural language commands into real browser actions, email automation, calendar scheduling, and more — powered by Google Gemini, LangChain, Playwright, FastAPI, and React.**

Built as part of the **SOC (Summer of Code)** program over 6 weeks, culminating in a production-grade full-stack final project.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![LangChain](https://img.shields.io/badge/LangChain-Agent-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)

</div>

---

## 📌 About This Project

This project is a **6-week progressive learning journey** that builds from basic Python scripting all the way to a full-stack AI-powered browser agent with:

- 🧠 **Smart AI Search** — Gemini-powered intent extraction that searches Google, YouTube, Medium, Reddit, GeeksforGeeks, Stack Overflow, GitHub, and more based on what you're actually looking for
- 📧 **Email Assistant** — Read, compose, and draft emails using Gmail integration and Gemini AI
- 📅 **Calendar Assistant** — Google Calendar integration with IST timezone, event listing, free slot finder, and natural language scheduling
- 📋 **Form Auto-Filler** — Detects form fields and fills them using stored user profile data
- 🔍 **Page Summarizer** — Extracts and summarizes webpage content using AI
- 🧠 **Persistent Memory** — SQLite-backed memory store that remembers your profile, notes, form history, and task history across sessions
- 🎨 **Premium React UI** — Glassmorphism design with 3D animations, dark mode, WebSocket real-time updates

---

## 🏗️ Project Structure

```
ai-browser-agent/
│
├── week1_python_warmup/           # Week 1 — Python fundamentals & async
│   ├── load_user_memory.py        # Async script to read & display user info
│   ├── user_info.json             # User data store (name, email, phone)
│   └── devtools_selectors/        # 6 CSS selector screenshots from Chrome DevTools
│
├── week2_playwright/              # Week 2 — Browser automation with Playwright
│   ├── script1_navigator.py       # Scrapes top 5 Hacker News articles → JSON
│   ├── script2_form_filler.py     # Auto-fills demoqa practice form from JSON
│   ├── script3_tab_manager.py     # Opens 5 tabs in parallel, captures titles
│   ├── form_data.json             # Form data used by the filler script
│   └── output/                    # Generated JSON + screenshots (proof of run)
│
├── week3_intent_parser/           # Week 3 — LLM-powered intent parsing
│   ├── intent_parser.py           # parse_intent() using Google Gemini API
│   ├── test_commands.py           # Runs 10 test commands → generates results
│   └── test_commands.md           # Output proof — 10 commands with JSON results
│
├── week4_langchain_agent/         # Week 4 — LangChain ReAct agent
│   ├── agent.py                   # LangChain agent with Gemini LLM + memory
│   ├── tools.py                   # 3 custom tools: navigate, click, type
│   ├── user_profile.json          # User profile for auto-fill (bonus feature)
│   └── memory_demo.md             # Proof of conversation memory across turns
│
├── week5_fastapi_server/          # Week 5 — FastAPI backend server
│   ├── main.py                    # FastAPI app with CORS, WebSocket, task runner
│   ├── agent_runner.py            # Background agent task execution engine
│   ├── models.py                  # SQLModel schemas (Task, UserProfile)
│   ├── database.py                # SQLite session management
│   ├── gmail_helper.py            # Gmail API integration helper
│   └── pdf_parser.py              # PDF text extraction utility
│
├── week6_react_ui/                # Week 6 — React frontend dashboard
│   ├── src/
│   │   ├── App.jsx                # Main app with sidebar navigation & routing
│   │   ├── App.css                # Premium glassmorphism CSS with 3D animations
│   │   └── components/
│   │       ├── CommandPanel.jsx    # Command input + WebSocket task launcher
│   │       ├── ActivityLog.jsx     # Real-time step-by-step task log display
│   │       ├── FormModule.jsx      # Form auto-fill module UI
│   │       ├── EmailModule.jsx     # Email read/compose module UI
│   │       ├── SummaryModule.jsx   # Page summarization module UI
│   │       ├── CalendarModule.jsx  # Calendar events & scheduling UI
│   │       ├── MemoryModule.jsx    # Memory storage viewer (profile, notes, forms)
│   │       └── ProfileSettings.jsx # User profile editor with save functionality
│   └── package.json
│
├── final_project/                 # 🏆 Final Integrated Project
│   ├── main.py                    # FastAPI app — all module routers mounted
│   ├── agent_runner.py            # AI-powered agent with smart search engine
│   ├── models.py                  # SQLModel schemas for tasks & profiles
│   ├── database.py                # SQLite database engine
│   ├── module1_form_filler/       # Form detection & auto-fill logic
│   ├── module2_email_assistant/   # Gmail read/compose with Gemini AI drafting
│   ├── module3_vision_assistant/  # Vision & page summarization module
│   ├── module4_calendar_assistant/# Google Calendar integration (IST timezone)
│   ├── module5_cross_module/      # Cross-module orchestration & routing
│   ├── module6_memory/            # SQLite-backed persistent memory store
│   └── data/                      # Runtime databases (memory.db)
│
├── tests/                         # Test suite
├── venv/                          # Python virtual environment
├── .gitignore
└── README.md
```

---

## 📅 Week-by-Week Breakdown

### 🟢 Week 1 — Python & Environment Setup

> **Goal:** Set up the development environment and learn Python async fundamentals.

- Configured Python 3.12 virtual environment with all required packages
- Built an **async script** using `asyncio.to_thread()` that reads user info from a JSON file and displays it in a formatted card
- Used Chrome DevTools to identify **CSS selectors** for 3 input fields, 2 buttons, and 1 dropdown on a practice form
- Captured 6 screenshots as proof of selector identification

**Key Concepts:** `asyncio`, `aiofiles`, JSON handling, Chrome DevTools, CSS selectors

---

### 🟡 Week 2 — Playwright Browser Automation

> **Goal:** Automate real browser interactions programmatically.

- **Script 1 (Navigator):** Opens Hacker News, scrapes the top 5 article titles and URLs, saves results to `output/top_articles.json`
- **Script 2 (Form Filler):** Reads form data from JSON and programmatically fills every field of the demoqa practice form — text inputs, dropdowns, radio buttons, checkboxes, date pickers — then takes a screenshot
- **Script 3 (Tab Manager):** Opens 5 different websites in parallel tabs using `asyncio.gather()`, captures each page title, then closes all tabs except the first
- All scripts use `async/await` patterns and handle timeout + missing-element errors gracefully

**Key Concepts:** Playwright, headless browser, web scraping, form automation, parallel tab management

---

### 🟠 Week 3 — Intent Parser with LLM

> **Goal:** Use an LLM to understand natural language commands and convert them to structured actions.

- Built `parse_intent(user_command)` that calls the **Google Gemini API** and returns structured JSON
- Output schema includes: `intent`, `target`, `parameters`, `needs_clarification`, `clarification_question`
- Engineered a system prompt with **5 few-shot examples** covering navigate, fill_form, click, email, and summarize intents
- **Bonus:** Handles ambiguous commands by setting `needs_clarification: true` and generating a specific follow-up question
- Tested with 10 diverse commands; all results documented in `test_commands.md`

**Key Concepts:** Prompt engineering, few-shot learning, structured output, intent classification, Gemini API

---

### 🔴 Week 4 — LangChain Agent with Memory

> **Goal:** Build an autonomous agent that can reason, plan, and execute multi-step browser tasks.

- Created **3 custom LangChain tools** wrapping Playwright actions:
  - `navigate_to` — Opens any URL in the browser
  - `click_element` — Clicks on elements using CSS selectors
  - `type_text` — Types text into input fields
- Agent uses **`ConversationBufferMemory`** — remembers all previous steps within a session, enabling multi-turn conversations
- Implements the **ReAct loop**: Reason → Act with tool → Observe result → Reason again
- **Bonus:** Reads `user_profile.json` and injects it into the system prompt so the agent can auto-fill forms with user data

**Key Concepts:** LangChain, ReAct pattern, tool-calling agents, conversation memory, system prompt injection

---

### 🟣 Week 5 — FastAPI Backend Server

> **Goal:** Build a production-grade REST API backend that serves the agent and all modules.

- Built a **FastAPI application** with CORS middleware, WebSocket support, and background task execution
- Implemented **SQLModel** schemas for `Task` and `UserProfile` with SQLite persistence
- Created a **WebSocket-based real-time update system** — the agent streams step-by-step progress to connected clients
- Added **Gmail integration** helper for reading and composing emails
- Built a **PDF parser** utility for extracting text from uploaded documents
- RESTful endpoints for task management (`POST /run`, `GET /tasks/{id}`), user profile CRUD, and health checks

**Key Concepts:** FastAPI, WebSocket, SQLModel/SQLite, CORS, background tasks, REST API design

---

### 🔵 Week 6 — React Frontend Dashboard

> **Goal:** Build a premium, interactive frontend that connects to the FastAPI backend.

- Designed a **glassmorphism dark-mode UI** with 3D rotating cube animations, ambient light effects, and floating particles
- Built **8 React components** each handling a distinct module:
  - `CommandPanel` — Natural language input with WebSocket connection for real-time task execution
  - `ActivityLog` — Live step-by-step display of agent actions with clickable "Visit" links
  - `FormModule` — Form auto-fill interface
  - `EmailModule` — Email reading and composition
  - `SummaryModule` — Page summarization
  - `CalendarModule` — Calendar events viewer with IST timezone
  - `MemoryModule` — Persistent memory viewer (profile, notes, form history)
  - `ProfileSettings` — User profile editor that syncs with memory store
- **Sidebar navigation** with active tab highlighting and smooth transitions
- Fully responsive layout with real-time WebSocket communication to the backend

**Key Concepts:** React 18, Vite, WebSocket client, component architecture, CSS animations, glassmorphism

---

## 🏆 Final Project — Integrated AI Browser Agent

The final project brings all 6 weeks together into a **single, cohesive full-stack application** with 6 integrated modules:

### Module 1: Form Auto-Filler
Detects form fields on any webpage and automatically fills them using the stored user profile. Supports text inputs, dropdowns, checkboxes, and more.

### Module 2: Email Assistant
Connects to Gmail API for reading inbox messages. Uses Gemini AI to draft intelligent email replies and compose new emails from natural language instructions.

### Module 3: Vision & Summary Assistant
Takes any webpage URL and generates an AI-powered summary of its content, extracting key points, main arguments, and important data.

### Module 4: Calendar Assistant
Full Google Calendar integration with **IST (Indian Standard Time)** timezone support:
- Lists upcoming events
- Finds free time slots
- Schedules new events from natural language (e.g., *"Schedule a meeting tomorrow at 3pm"*)

### Module 5: Cross-Module Orchestration
Routes user commands to the appropriate module based on intent analysis. Enables multi-module workflows where one command can trigger actions across multiple modules.

### Module 6: Persistent Memory Store
SQLite-backed memory system that remembers everything across sessions:
- **User Profile** — Name, email, phone, address, resume text
- **Agent Notes** — AI-generated summaries and observations
- **Form History** — Records of previously filled forms
- **Task History** — Log of all executed commands and their results
- **Preferences** — User preferences learned over time

### 🧠 Smart AI Search Engine
The crown feature — an intelligent search system that:
1. Uses **Gemini AI** to extract the real search intent from any command
2. Searches **DuckDuckGo** with the cleaned query for 5 highly relevant results
3. **Dynamically generates platform links** based on the topic type:

| Topic Type | Platforms Searched |
|---|---|
| **All queries** | Google, YouTube, Medium Blogs, Reddit |
| **Tech / Programming** | + GeeksforGeeks, Stack Overflow, GitHub |
| **Research / Academic** | + Google Scholar |
| **News / Current Events** | + Google News |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Google Gemini API key ([Get free key](https://aistudio.google.com))

### 1. Clone the repository
```bash
git clone https://github.com/gitprashanthub69/ai-agent-browser.git
cd ai-agent-browser
```

### 2. Set up Python environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### 3. Set your Gemini API key
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-api-key-here"
```

### 4. Start the backend server
```bash
cd final_project
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Start the React frontend
```bash
cd week6_react_ui
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

### 6. Open in your browser
- **Frontend UI:** [http://localhost:3000](http://localhost:3000)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💡 Example Commands

Try these in the Command Center:

| Command | What Happens |
|---|---|
| `Search Google for the best AI tools` | AI extracts "best AI tools", searches DuckDuckGo, generates Google/YouTube/Medium/Reddit/GFG/StackOverflow links |
| `Search YouTube for the latest Mr Beast video` | Searches YouTube specifically for Mr Beast videos with direct links |
| `Fill the contact form with my profile details` | Reads saved profile and auto-fills detected form fields |
| `Summarize the current page` | Generates an AI-powered summary of the current webpage |
| `Schedule a meeting tomorrow at 3pm` | Creates a Google Calendar event in IST timezone |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12** | Core backend language |
| **FastAPI** | REST API + WebSocket server |
| **React 18 + Vite** | Frontend UI framework |
| **Google Gemini API** | LLM for intent parsing, search extraction, email drafting |
| **LangChain** | Agent framework (ReAct pattern + memory) |
| **Playwright** | Browser automation engine |
| **SQLModel + SQLite** | Database ORM and local storage |
| **DuckDuckGo Search** | Live web search API |
| **Google Calendar API** | Calendar event management |
| **Gmail API** | Email reading and composition |
| **WebSocket** | Real-time agent-to-UI communication |

---

## 📁 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/run` | Start a new agent task |
| `GET` | `/tasks/{id}` | Get task status and steps |
| `GET` | `/user/profile` | Read saved user profile |
| `POST` | `/user/profile` | Create/update user profile |
| `WS` | `/ws/{task_id}` | WebSocket for real-time task updates |
| `GET` | `/memory/context` | Get full memory context (profile + notes + forms) |
| `POST` | `/memory/notes` | Save a new agent note |
| `GET` | `/memory/search?q=` | Search across all memory stores |
| `GET` | `/api/calendar/events` | List upcoming calendar events (IST) |
| `POST` | `/api/calendar/schedule` | Schedule event from natural language |
| `POST` | `/api/email/read` | Read recent emails |
| `POST` | `/api/email/compose` | Compose email with AI |
| `POST` | `/api/summary/` | Summarize a webpage |

---

## 👤 Author

**Sagar** — SOC (Summer of Code) Participant

- GitHub: [@gitprashanthub69](https://github.com/gitprashanthub69)

---

## 📜 License

This project is built for educational purposes as part of the SOC program.
