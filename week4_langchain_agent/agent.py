"""
Week 4 — LangChain Agent
- Uses Google Gemini as the LLM (free tier, no card needed)
- 3 custom Playwright tools: navigate_to, click_element, type_text
- Conversation memory so the agent remembers previous steps
- Bonus: reads user profile from user_profile.json
"""

import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import TOOLS

# ── Load user profile (Bonus feature) ────────────────────────────────────────

def load_user_profile(path: str = "user_profile.json") -> dict:
    """Load user profile from JSON file. Returns empty dict if file missing."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"⚠️  Could not parse {path} — using empty profile.")
        return {}


# ── Build the agent ───────────────────────────────────────────────────────────

def build_agent():
    """Creates and returns a LangChain AgentExecutor with memory."""

    # 1. LLM — Gemini Flash (free tier)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.environ.get("GEMINI_API_KEY"),
        temperature=0,
    )

    # 2. User profile for context
    profile = load_user_profile()
    profile_str = json.dumps(profile, indent=2) if profile else "No profile loaded."

    # 3. System prompt
    system_prompt = f"""You are an AI browser agent that helps users complete tasks on the web.

You have access to 3 browser tools:
- navigate_to: go to any URL
- click_element: click any element by CSS selector
- type_text: type text into any field (format: selector|||text)

User profile (use this to fill in personal details when needed):
{profile_str}

Always:
1. Think step-by-step before acting
2. Use the right tool for each step
3. Report what you did after each action
4. If a task is ambiguous, ask a clarifying question before acting

You remember everything from earlier in this conversation.
"""

    # 4. Prompt template with memory placeholder
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 5. Conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    # 6. Agent + executor
    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        memory=memory,
        verbose=True,          # prints reasoning + tool calls
        handle_parsing_errors=True,
        max_iterations=6,      # prevent infinite loops
    )

    return executor


# ── Run the agent ─────────────────────────────────────────────────────────────

def run_agent():
    """Interactive loop — type commands, agent executes them."""
    print("\n🤖 AI Browser Agent — Week 4")
    print("Type a command (or 'quit' to exit)\n")

    agent = build_agent()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        try:
            result = agent.invoke({"input": user_input})
            print(f"\n Agent: {result['output']}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    run_agent()
