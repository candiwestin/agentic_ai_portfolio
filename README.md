# Agentic AI Portfolio

A monorepo of production-ready agentic AI pipelines built with LangChain, LangGraph, FastMCP, CrewAI, and Groq. Each pipeline demonstrates a distinct architecture pattern for building intelligent, tool-using AI systems — from basic retrieval to multi-agent collaboration.

**Live Demo:** [agentic-ai-portfolio-ui.vercel.app](https://agentic-ai-portfolio-ui.vercel.app)
**API:** [agentic-ai-portfolio-api.onrender.com](https://agentic-ai-portfolio-api.onrender.com/health)

---

## About

Built by **Candi Westin** — Senior Data & AI Engineer with 20+ years in data engineering and a passion for agentic AI systems. This portfolio represents hands-on engineering work across the full agentic AI stack: vector databases, LLM orchestration, intelligent routing, protocol-based tool use, and multi-agent collaboration. Every pipeline is deployed and interactive.

---

## Pipelines

| # | Pipeline | Architecture Pattern | Vector DB |
|---|----------|---------------------|-----------|
| 01 | [Basic RAG](pipelines/basic_rag_workflow/README.md) | Document ingestion → FAISS retrieval → LLM generation | NFL Wikipedia (1,272 chunks) |
| 02 | [LangGraph Chat](pipelines/langgraph_chat_workflow/README.md) | Stateful conversational agent with persistent memory | None — general LLM knowledge |
| 03 | [Agentic RAG](pipelines/agentic_rag_workflow/README.md) | LLM router → vector search / web search / direct LLM | Mountain biking guide + Wikipedia (171 chunks) |
| 04 | [MCP Workflow](pipelines/mcp_agent_workflow/README.md) | FastMCP client-server agent over SSE protocol | MCP documentation (149 chunks) |
| 05 | [CrewAI](pipelines/crewai_workflow/README.md) | 4-agent role-based collaboration: Researcher → Analyst → Critic → Writer | None — agent-based reasoning |

---

## Architecture

```
Agentic AI Portfolio UI (React + Vite — Vercel)
└── calls ──▶ FastAPI (Render)
              ├── /api/basic-rag        ← FAISS retrieval + Groq LLM
              ├── /api/langgraph-chat   ← Groq LLM with conversation history
              └── /api/agentic-rag      ← LLM router + FAISS + Tavily web search

Shared Utilities (shared/utils/)
├── llm_utils.py          ← Groq LLM initialization
├── vector_utils.py       ← FAISS create/load
├── retrieval_utils.py    ← Chunk retrieval and formatting
├── loader_utils.py       ← PDF and web document loaders
├── chunking_utils.py     ← Text splitting
└── web_search_utils.py   ← Tavily web search
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq (llama-3.3-70b-versatile) |
| Orchestration | LangChain, LangGraph |
| Vector DB | FAISS (committed to repo) |
| Embeddings | HuggingFace sentence-transformers/all-MiniLM-L6-v2 |
| Multi-agent | CrewAI |
| Tool protocol | FastMCP over SSE |
| Web search | Tavily |
| API | FastAPI + Uvicorn |
| UI | React + Vite (separate repo) |
| Deployment | Render (API), Vercel (UI) |

---

## Project Structure

```
agentic_ai_portfolio/
│
├── shared/                        # Utilities shared across all pipelines
│   └── utils/
│       ├── llm_utils.py
│       ├── loader_utils.py
│       ├── chunking_utils.py
│       ├── vector_utils.py
│       ├── retrieval_utils.py
│       ├── graph_utils.py
│       └── web_search_utils.py
│
├── pipelines/
│   ├── basic_rag_workflow/
│   │   └── storage/faiss_basic/       # NFL vector database
│   ├── langgraph_chat_workflow/
│   ├── agentic_rag_workflow/
│   │   └── storage/faiss_agentic/     # Mountain biking vector database
│   ├── mcp_agent_workflow/
│   │   └── storage/faiss_mcp/         # MCP documentation vector database
│   └── crewai_workflow/
│
├── api/
│   ├── main.py                        # FastAPI application
│   └── requirements.txt
│
├── data/
│   └── sample_files/                  # Source PDFs
│
├── .python-version                    # Python 3.11.9 (required)
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Requirements

- Python **3.11** — required for HuggingFace/LangChain compatibility
- [Groq API key](https://console.groq.com/)
- [Tavily API key](https://app.tavily.com/)

---

## Local Setup

### 1. Clone and create virtual environment

```bash
git clone https://github.com/candiwestin/agentic_ai_portfolio.git
cd agentic_ai_portfolio
python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
```

### 2. Install PyTorch first

PyTorch must be installed before the rest of the dependencies:

```bash
pip install torch==2.10.0
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
USER_AGENT=agentic_ai_portfolio/1.0
DEFAULT_MODEL=llama-3.3-70b-versatile
CREWAI_MODEL=groq/llama-3.3-70b-versatile
```

### 5. Build vector databases

```bash
python -m pipelines.basic_rag_workflow.src.setup_vector_db
python -m pipelines.agentic_rag_workflow.src.setup_vector_db
python -m pipelines.mcp_agent_workflow.src.data.load_documents
```

### 6. Run a pipeline

```bash
# Basic RAG
python -m pipelines.basic_rag_workflow.src.rag_pipeline

# Agentic RAG
python -m pipelines.agentic_rag_workflow.src.agentic_workflow

# LangGraph Chat
python -m pipelines.langgraph_chat_workflow.src.workflow

# CrewAI (provide a topic)
python -m pipelines.crewai_workflow.src.crewai_version "your topic here"
```

### 7. Run the API locally

```bash
cd api
uvicorn main:app --reload --port 8000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/HEAD | `/health` | Health check — returns `{"status": "ok", "dbs_loaded": true}` |
| POST | `/api/basic-rag` | NFL knowledge base query → `{answer, sources}` |
| POST | `/api/langgraph-chat` | Stateful chat → `{response}` |
| POST | `/api/agentic-rag` | Routed query → `{answer, route}` where route is `vector_db`, `web_search`, or `generic` |

---

## Common Issues

**Wrong Python version**
This project requires Python 3.11. Using 3.12+ causes HuggingFace/Pydantic dependency conflicts.

**`ModuleNotFoundError: No module named 'shared'`**
Run `pip install -e .` from the project root with the venv activated.

**Rate limit errors with Groq**
The free tier has token-per-minute limits. CrewAI workflows are particularly token-heavy — wait 30-60 seconds and retry.

**Vector database not found**
Run the setup scripts in step 5 above. Each pipeline needs its own database built before use.