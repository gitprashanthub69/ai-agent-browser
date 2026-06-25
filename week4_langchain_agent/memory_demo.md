# Week 4 — Conversation Memory Demo

This file shows that the LangChain agent remembers previous steps
across a multi-turn conversation (not just one message at a time).

---

## How memory works in this agent

`ConversationBufferMemory` stores the full chat history and passes it
to the LLM on every turn via the `chat_history` placeholder in the prompt.
This means the agent can refer back to what it already did.

---

## Sample session (run `python agent.py` to reproduce)

**Turn 1**
```
You: Go to google.com and search for AI news
Agent: ✅ Navigated to https://google.com
       ✅ Clicked element: input[name=q]
       ✅ Typed 'AI news' into input[name=q]
       ✅ Clicked element: button[type=submit]
       Done! I searched for 'AI news' on Google.
```

**Turn 2**
```
You: Now click the first result
Agent: (remembers it just searched Google)
       ✅ Clicked element: h3:first-of-type
       Clicked the first search result.
```

**Turn 3**
```
You: Fill the contact form with my details
Agent: (remembers user profile was loaded)
       ✅ Typed 'Your Name' into #name
       ✅ Typed 'your@email.com' into #email
       ✅ Typed '9999999999' into #phone
       Filled the contact form with your profile details.
```

---

## Memory implementation

```python
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)
```

The `chat_history` key is injected into every LLM call via:
```python
MessagesPlaceholder(variable_name="chat_history")
```

This gives the agent full context of everything said so far,
enabling multi-step tasks like: navigate → search → click → fill form.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `agent.py` | Main agent — LLM + tools + memory wired together |
| `tools.py` | 3 custom LangChain tools (navigate, click, type) |
| `user_profile.json` | User data the agent reads to fill forms (Bonus) |
| `memory_demo.md` | This file — proof memory works across turns |
