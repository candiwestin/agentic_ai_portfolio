# Agentic RAG Workflow

A LangGraph-based agentic pipeline that intelligently routes user queries to the most appropriate data source. Instead of always querying the vector database, this system classifies each query and routes it to vector search, web search, or a direct LLM response — then synthesizes a final answer with conversation memory.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## How It Works

Each query flows through a compiled LangGraph state machine:

```
User Query
    │
    ▼
┌─────────┐
│ Router  │  Classifies query: vector_db / web_search / generic_search
└────┬────┘
     │
     ├──► vector_db node      — FAISS similarity search on loaded documents
     ├──► web_search node     — Tavily web search for current information
     └──► generic_search node — Direct LLM response from training knowledge
                │
                ▼
        ┌───────────────┐
        │ Final Response │  Synthesizes answer with conversation history
        └───────────────┘
```

**Routing logic:**
- `vector_db` — technical questions about AI, ML, LangGraph, mountain biking, nutrition, or loaded documents
- `web_search` — questions with time indicators: "today", "latest", "current", news, weather, scores
- `generic_search` — simple questions, greetings, basic math, definitions

---

## Pre-loaded Documents

The database (`storage/faiss_agentic`) contains:

| Document | Content |
|----------|---------|
| LangGraph Docs | Why LangGraph, concepts, state machines, use cases |
| Mountain Bike Wikipedia | History, types, components, techniques |
| Nutrition Wikipedia | Macronutrients, micronutrients, dietary guidelines |

---

## Setting Up the Vector Database

```bash
python -m pipelines.agentic_rag_workflow.src.setup_vector_db
```

---

## Running the Pipeline

```bash
source .venv/bin/activate
cd /path/to/agentic_ai_portfolio
python -m pipelines.agentic_rag_workflow.src.agentic_workflow
```

---

## Sample Questions

### Routes to vector_db
```
Why use LangGraph over LangChain?
What is a state machine in LangGraph?
What are the different types of mountain bikes?
What nutrients are essential for human health?
What is the difference between carbohydrates and proteins?
```

### Routes to web_search
```
What are the latest developments in AI today?
Who won the most recent cycling race?
What is the current recommended daily vitamin D intake?
```

### Routes to generic_search
```
What is 15 multiplied by 7?
Tell me a joke.
What is the capital of France?
```

---

## Conversation Memory

This pipeline maintains conversation history across turns. Each response takes into account the last 3 exchanges:

```
You: What is LangGraph?
Agent: [detailed answer]

You: How does that compare to LangChain?
Agent: [answer referencing the previous context]
```

---

## Pipeline Structure

```
pipelines/agentic_rag_workflow/
├── src/
│   ├── agentic_workflow.py       # Full LangGraph pipeline — entry point
│   └── setup_vector_db.py        # Build FAISS index from source documents
└── storage/
    └── faiss_agentic/            # Pre-built vector database
        ├── index.faiss
        └── index.pkl
```

**Shared utilities used:**

```
shared/utils/llm_utils.py         # LLM initialization, DEFAULT_MODEL
shared/utils/vector_utils.py      # FAISS vector store loading
shared/utils/retrieval_utils.py   # Chunk retrieval and formatting
shared/utils/web_search_utils.py  # Tavily web search
shared/utils/graph_utils.py       # Workflow diagram generation
```

---

## Workflow Diagram

A PNG diagram of the LangGraph workflow is auto-generated at startup:

```
outputs/agentic_workflow_diagram.png
```

---

## Common Issues

**`ModuleNotFoundError: No module named 'shared'`**
Run `pip install -e .` from the project root with the venv activated.

**FAISS index not found**
Run the setup script: `python -m pipelines.agentic_rag_workflow.src.setup_vector_db`

**Web search returning no results**
Verify your `TAVILY_API_KEY` is set correctly in `.env`.