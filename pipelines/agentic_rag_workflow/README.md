# Agentic RAG Workflow

A LangGraph-based agentic pipeline that intelligently routes user queries to the most appropriate data source. Instead of always querying the vector database, this system classifies each query and routes it to vector search, web search, or a direct LLM response — then synthesizes a final answer.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## How It Works

Each query flows through a compiled LangGraph state machine:

```
User Query
    │
    ▼
┌─────────┐
│ Router  │  Classifies query: vector_db / web_search / generic
└────┬────┘
     │
     ├──► vector_db node      — FAISS similarity search on mountain biking knowledge base
     ├──► web_search node     — Tavily web search for current information
     └──► generic node        — Direct LLM response from training knowledge
                │
                ▼
        ┌───────────────┐
        │ Final Response │  Synthesizes answer from retrieved context
        └───────────────┘
```

**Routing logic:**
- `vector_db` — mountain biking topics: gear, techniques, trails, bike types, racing
- `web_search` — questions requiring current information: news, events, latest results
- `generic` — simple questions, greetings, definitions, general knowledge

---

## Knowledge Base

The vector database (`storage/faiss_agentic`) contains **171 chunks** sourced from:

| Source | Content |
|--------|---------|
| Mountain Biking Guide (PDF) | Gear, techniques, trail ratings, safety, maintenance |
| Wikipedia — Mountain Bike | History, bike types, components, disciplines |
| Wikipedia — Mountain Bike Racing | Race formats, events, notable riders |

---

## Setting Up the Vector Database

```bash
python -m pipelines.agentic_rag_workflow.src.setup_vector_db
```

---

## Running the Pipeline

```bash
source .venv/bin/activate
python -m pipelines.agentic_rag_workflow.src.agentic_workflow
```

---

## Sample Questions

### Routes to vector_db
```
What are the best mountain bikes for beginners?
What gear do I need for mountain biking?
What is the difference between hardtail and full suspension?
How do I choose the right trail difficulty?
What is cross-country mountain bike racing?
```

### Routes to web_search
```
Who won the latest UCI Mountain Bike World Cup?
What are the most popular mountain bike trails right now?
What are the newest mountain bike models this year?
```

### Routes to generic
```
What is the capital of France?
How many inches in a foot?
Tell me a joke.
```

---

## API Usage

This pipeline is exposed via the portfolio API at `POST /api/agentic-rag`:

```json
// Request
{
  "query": "What are the best mountain bikes for beginners?"
}

// Response
{
  "answer": "For beginners, the best mountain bikes...",
  "route": "vector_db"
}
```

The `route` field shows which data source was used: `vector_db`, `web_search`, or `generic`.

---

## Pipeline Structure

```
pipelines/agentic_rag_workflow/
├── src/
│   ├── config.py                 # Source URLs, PDF paths, configuration
│   ├── agentic_workflow.py       # Full LangGraph pipeline — entry point
│   └── setup_vector_db.py        # Build FAISS index from configured sources
└── storage/
    └── faiss_agentic/            # Pre-built vector database
        ├── index.faiss
        └── index.pkl
```

**Shared utilities used:**
```
shared/utils/llm_utils.py         # LLM initialization
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