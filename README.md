# AI Browser Agent

This repository contains a multi-week project that builds an automated browser agent with progressively more advanced capabilities.

## Project Overview

- **Week 1:** basic user info handling and DevTools selector screenshots
- **Week 2:** Playwright browser automation scripts with real output evidence
- **Week 3:** intent parsing using an LLM-based parser and test command outputs
- **Week 4:** LangChain-based browser agent with tools, memory, and user profile support

## Repository Structure

- `load_user_memory.py` — Week 1 script to print user info in a formatted box
- `devtools_selectors/` — Week 1 DevTools screenshot files
- `week2_playwright/` — Week 2 Playwright scripts and input/output data
  - `script1_navigator.py`
  - `script2_form_filler.py`
  - `script3_tab_manager.py`
  - `form_data.json`
  - `output/` — generated execution evidence
- `week3_intent_parser/` — Week 3 intent parser and test runner
  - `intent_parser.py`
  - `test_commands.py`
  - `test_commands.md`
- `week4_langchain_agent/` — Week 4 LangChain agent implementation
  - `agent.py`
  - `tools.py`
  - `user_profile.json`
  - `memory_demo.md`
- `requirements.txt` — full Python dependency list for the environment

## What has been completed

### Week 1

- `load_user_memory.py` is present and runnable
- `devtools_selectors/` contains browser selector screenshots

### Week 2

- 3 Playwright automation scripts are available
- `week2_playwright/output/` contains generated evidence files:
  - `top_articles.json`
  - `form_before_submit.png`
  - `tab_titles.json`

### Week 3

- `intent_parser.py` implements a parser with Anthropic fallback
- `test_commands.py` generates real command outputs
- `test_commands.md` contains the actual output from running the script

### Week 4

- `agent.py`, `tools.py`, `user_profile.json`, and `memory_demo.md` are present
- `memory_demo.md` documents how the agent remembers context

## Setup Instructions

### 1. Create and activate your virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. If you need Playwright for Week 2

```powershell
pip install playwright
playwright install chromium
```

### 4. If you need Anthropic/Gemini keys

- Set `ANTHROPIC_API_KEY` for Week 3 if using Anthropic
- Set `GEMINI_API_KEY` for Week 4

### 5. Run each week

Week 1:
```powershell
python load_user_memory.py
```

Week 2:
```powershell
python week2_playwright/script1_navigator.py
python week2_playwright/script2_form_filler.py
python week2_playwright/script3_tab_manager.py
```

Week 3:
```powershell
cd week3_intent_parser
python test_commands.py
```

Week 4:
```powershell
cd week4_langchain_agent
python agent.py
```

## Notes for Mentors

- `requirements.txt` is intentionally long and reflects a real Python environment with installed dependencies.
- `test_commands.md` contains real output from running the Week 3 test script.
- `week2_playwright/output/` contains screenshots and JSON files showing successful Playwright execution.

## Contact

If you want to update the user profile for the Week 4 agent, edit `week4_langchain_agent/user_profile.json`.
