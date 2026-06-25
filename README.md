# AI Browser Agent — 6-Week Learning Project

An agentic AI browser assistant built as part of the SOC (Summer of Code) program.
The agent converts natural language commands into browser actions using LLMs and Playwright.

---

## Project Structure

```
ai-browser-agent/
├── week1_python_warmup/
│   ├── load_user_memory.py       # Async script that reads and prints user info
│   ├── user_info.json            # User data (name, email, phone, address)
│   └── devtools_selectors/       # 6 CSS selector screenshots from Chrome DevTools
│       ├── input1_firstname.png
│       ├── input2_lastname.png
│       ├── input3_email.png
│       ├── button1_submit.png
│       ├── button2_xxx.png
│       └── dropdown1_state.png
│
├── week2_playwright/
│   ├── script1_navigator.py      # Scrapes top 5 Hacker News articles → JSON
│   ├── script2_form_filler.py    # Fills demoqa practice form from JSON
│   ├── script3_tab_manager.py    # Opens 5 tabs in parallel, captures titles
│   ├── form_data.json            # Data used by the form filler script
│   └── output/                   # Generated JSON + screenshots (proof of run)
│
├── week3_intent_parser/
│   ├── intent_parser.py          # parse_intent() function using Gemini API
│   ├── test_commands.py          # Runs 10 commands and generates test_commands.md
│   └── test_commands.md          # Output proof — 10 commands with JSON results
│
├── week4_langchain_agent/
│   ├── agent.py                  # LangChain agent with Gemini LLM + memory
│   ├── tools.py                  # 3 custom tools: navigate_to, click_element, type_text
│   ├── user_profile.json         # User profile store (Bonus feature)
│   └── memory_demo.md            # Proof that conversation memory works across turns
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-browser-agent.git
cd ai-browser-agent
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Set your Gemini API key
Get a free key at [aistudio.google.com](https://aistudio.google.com)

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIza..."

# Mac/Linux
export GEMINI_API_KEY="AIza..."
```

---

## How to Run Each Week

### Week 1 — Async User Memory Script
```bash
cd week1_python_warmup
python load_user_memory.py
```
Expected output: your info printed in a bordered card format.

### Week 2 — Playwright Browser Automation
```bash
cd week2_playwright
python script1_navigator.py    # scrapes Hacker News → output/top_articles.json
python script2_form_filler.py  # fills demoqa form → output/form_screenshot.png
python script3_tab_manager.py  # opens 5 tabs, prints titles
```

### Week 3 — Intent Parser
```bash
cd week3_intent_parser
python test_commands.py        # runs 10 commands → generates test_commands.md
```

### Week 4 — LangChain Agent
```bash
cd week4_langchain_agent
python agent.py                # interactive agent — type commands, agent executes
```
Example commands to try:
- `Go to google.com and search for AI news`
- `Now click the first result`
- `Fill the contact form with my details`

---

## Week Summaries

### Week 1 — Python & Environment Setup
- Python 3.12 virtual environment with `requests`
- Async script using `asyncio.to_thread()` to read user JSON
- Identified CSS selectors for 3 inputs, 2 buttons, 1 dropdown using Chrome DevTools

### Week 2 — Playwright Browser Automation
- Script 1: navigates to Hacker News, extracts top 5 article titles and links, saves to JSON
- Script 2: fills every field of the demoqa practice form from a JSON file, takes screenshot
- Script 3: opens 5 tabs in parallel using `asyncio.gather()`, captures each title, closes all but first
- All scripts use `async def`, handle timeout and missing-element errors

### Week 3 — Intent Parser with LLM
- `parse_intent(user_command)` calls Google Gemini API and returns structured JSON
- Schema: `intent`, `target`, `parameters`, `needs_clarification`, `clarification_question`
- 5 few-shot examples in system prompt covering navigate, fill_form, click, email, summarize
- Bonus: ambiguous commands trigger `needs_clarification: true` with a specific question
- Tested with 10 diverse commands, results in `test_commands.md`

### Week 4 — LangChain Agent with Memory
- 3 custom LangChain tools wrapping Playwright actions
- Agent uses `ConversationBufferMemory` — remembers all previous steps in the session
- Bonus: reads `user_profile.json` and injects it into the system prompt for auto-fill tasks
- Full ReAct loop: Reason → Act with tool → Observe result → Reason again

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| Playwright | Browser automation |
| Google Gemini API | LLM for intent parsing and agent reasoning |
| LangChain | Agent framework (ReAct pattern + memory) |
| BeautifulSoup4 | HTML parsing |
| asyncio | Async/await throughout |

---

## Blockers & Notes

- Week 2 scripts require `playwright install chromium` on your local machine
- Gemini API key required for Week 3 and Week 4 (free at aistudio.google.com)
- Week 4 tools simulate browser actions — full Playwright integration comes in Week 5
