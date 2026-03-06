# LangGraph Chat Workflow

A clean, minimal conversational agent built with LangGraph. Demonstrates state-managed dialogue using a compiled graph workflow where each message flows through a single LLM node and state is tracked across the conversation.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## How It Works

```
User Input
    │
    ▼
┌──────────┐
│  START   │
└────┬─────┘
     │
     ▼
┌──────────┐
│ chatbot  │  LLM processes messages and returns response
└────┬─────┘
     │
     ▼
┌──────────┐
│   END    │
└──────────┘
```

LangGraph manages message state automatically using `add_messages`, which appends each new message to the conversation history. This gives the agent memory across turns without any manual state management.

---

## Running the Pipeline

```bash
source .venv/bin/activate
cd /path/to/agentic_ai_portfolio
python -m pipelines.langgraph_chat_workflow.src.workflow
```

---

## Sample Conversations

```
Enter your question: What is LangGraph?
Response: LangGraph is a library for building stateful, multi-actor applications...

Enter your question: How does it differ from LangChain?
Response: While LangChain focuses on chaining LLM calls...

Enter your question: Give me a simple example
Response: Here is a minimal LangGraph example...
```

The agent maintains context across turns so follow-up questions work naturally.

---

## Model Selection

The Streamlit UI page allows switching between models at runtime:

| Model | Speed | Quality |
|-------|-------|---------|
| `llama-3.3-70b-versatile` | Fast | High |
| `llama-3.1-8b-instant` | Very fast | Good |

From the CLI, the model is set via `DEFAULT_MODEL` in `.env`.

---

## Workflow Diagram

A PNG diagram is auto-generated at startup:

```
outputs/basic_workflow_diagram.png
```

The diagram only regenerates if the workflow structure has changed (hash-based caching).

---

## Pipeline Structure

```
pipelines/langgraph_chat_workflow/
└── src/
    └── workflow.py               # Full LangGraph chatbot — entry point
```

**Shared utilities used:**

```
shared/utils/llm_utils.py         # LLM initialization, DEFAULT_MODEL
shared/utils/graph_utils.py       # Workflow diagram generation
```

---

## Common Issues

**`ModuleNotFoundError: No module named 'shared'`**
Run `pip install -e .` from the project root with the venv activated.

**`GROQ_API_KEY` not found**
Make sure `.env` is in the project root and contains `GROQ_API_KEY=your_key_here`.

**Diagram not generating**
Make sure the `outputs/` directory exists at the project root:
```bash
mkdir -p outputs
```