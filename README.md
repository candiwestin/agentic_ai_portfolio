# Agentic AI Portfolio

A monorepo of production-ready agentic AI pipelines built with LangChain, LangGraph, FastMCP, CrewAI, and Groq. Each pipeline demonstrates a different architecture pattern for building intelligent, tool-using AI systems.

**Built by Candi Westin — Senior Data/AI Engineer**

---

## Pipelines

| Pipeline | Description | Run Command |
|----------|-------------|-------------|
| [MCP Agent Workflow](pipelines/mcp_agent_workflow/README.md) | Client-server agent using FastMCP + SSE. Tools exposed over MCP protocol. | See pipeline README |
| [Basic RAG Workflow](pipelines/basic_rag_workflow/README.md) | Document ingestion, FAISS vector search, and contextual LLM responses. | `python -m pipelines.basic_rag_workflow.src.rag_pipeline` |
| [Agentic RAG Workflow](pipelines/agentic_rag_workflow/README.md) | LangGraph router that intelligently selects vector search, web search, or direct LLM. | `python -m pipelines.agentic_rag_workflow.src.agentic_workflow` |
| [LangGraph Chat Workflow](pipelines/langgraph_chat_workflow/README.md) | State-managed conversational agent using a compiled LangGraph workflow. | `python -m pipelines.langgraph_chat_workflow.src.workflow` |
| [CrewAI Workflow](pipelines/crewai_workflow/README.md) | Multi-agent role-based system. 4 agents collaborate sequentially to research and produce a compliance-reviewed policy document on any topic. | `python -m pipelines.crewai_workflow.src.crewai_version "your topic here"` |

---

## Portfolio UI

All pipelines are showcased in a unified Streamlit application with one page per pipeline.
```bash
streamlit run app/main.py
```

The app opens in your browser automatically. Navigate between pipelines using the sidebar:

| Page | Pipeline | Notes |
|------|----------|-------|
| 1 — Basic RAG | basic_rag_workflow | Load pre-loaded database or enter a custom URL |
| 2 — LangGraph Chat | langgraph_chat_workflow | Stateful conversational agent, no setup required |
| 3 — Agentic RAG | agentic_rag_workflow | Load vector database, then ask any question |
| 4 — MCP Agent | mcp_agent_workflow | Requires MCP server running separately (see below) |
| 5 — CrewAI | crewai_workflow | Enter any policy topic and watch 4 agents collaborate |

### Running the MCP page

The MCP page shows a live server status indicator. To see it online, start the server in a separate terminal before launching Streamlit:
```bash
# Terminal 1 — start MCP server
source .venv/bin/activate
python -m pipelines.mcp_agent_workflow.src.mcp.mcp_server

# Terminal 2 — start Streamlit
source .venv/bin/activate
streamlit run app/main.py
```

---

## Vector Databases

Each RAG pipeline maintains its own named vector database under its `storage/` directory. They are independent and contain different content:

| Pipeline | Database | Content |
|----------|----------|---------|
| basic_rag_workflow | `storage/faiss_basic` | IBM Agentic AI article, NASA ISS page, Attention Is All You Need paper |
| agentic_rag_workflow | `storage/faiss_agentic` | LangGraph docs, Mountain biking Wikipedia, Nutrition Wikipedia |
| mcp_agent_workflow | `storage/faiss_mcp` | Deloitte Company Profile PDF |

### Building the databases

Run these once after cloning:

```bash
# Basic RAG
python -m pipelines.basic_rag_workflow.src.setup_multi_docs

# Agentic RAG
python -m pipelines.agentic_rag_workflow.src.setup_vector_db

# MCP
python -m pipelines.mcp_agent_workflow.src.data.load_documents
```

---

## Requirements

- Python **3.11** (required — other versions cause HuggingFace dependency conflicts)
- `pip` 23+
- A [Groq API key](https://console.groq.com/)
- A [Tavily API key](https://app.tavily.com/)
- A `USER_AGENT` string (any descriptive string, e.g. `agentic_ai_portfolio/1.0`)

---

## Environment Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd agentic_ai_portfolio
```

### 2. Confirm Python 3.11 is available

```bash
python3.11 --version
# Expected: Python 3.11.x
```

If not installed:

```bash
sudo apt install python3.11 python3.11-venv python3.11-dev
```

### 3. Create a virtual environment

```bash
python3.11 -m venv .venv
```

Activate it:

| Platform | Command |
|----------|---------|
| Linux / macOS | `source .venv/bin/activate` |
| Windows (CMD) | `.venv\Scripts\activate.bat` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

### 4. Upgrade pip

```bash
pip install --upgrade pip
```

### 5. Install PyTorch first

PyTorch must be installed before the rest of the dependencies:

```bash
pip install torch==2.10.0
```

### 6. Install all dependencies

```bash
pip install -r requirements.txt
```

### 7. Install the project as an editable package

This allows all pipelines to resolve imports from `shared/`:

```bash
pip install -e .
```

### 8. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
USER_AGENT=agentic_ai_portfolio/1.0
DEFAULT_MODEL=llama-3.3-70b-versatile
CREWAI_MODEL=groq/llama-3.3-70b-versatile
```

### 9. Build vector databases

```bash
python -m pipelines.basic_rag_workflow.src.setup_multi_docs
python -m pipelines.agentic_rag_workflow.src.setup_vector_db
python -m pipelines.mcp_agent_workflow.src.data.load_documents
```

---

## Project Structure

```
agentic_ai_portfolio/
│
├── shared/                        # Code shared across all pipelines
│   └── utils/
│       ├── llm_utils.py           # LLM initialization (Groq), DEFAULT_MODEL
│       ├── loader_utils.py        # PDF and web document loaders
│       ├── chunking_utils.py      # Text splitting utilities
│       ├── vector_utils.py        # FAISS vector store utilities
│       ├── retrieval_utils.py     # Chunk retrieval and formatting
│       ├── graph_utils.py         # LangGraph visualization
│       └── web_search_utils.py    # Tavily web search utilities
│
├── pipelines/
│   ├── mcp_agent_workflow/        # FastMCP client-server agent
│   │   └── storage/faiss_mcp/     # Deloitte PDF vector database
│   ├── basic_rag_workflow/        # Basic RAG pipeline
│   │   └── storage/faiss_basic/   # Multi-document vector database
│   ├── agentic_rag_workflow/      # Agentic RAG with router
│   │   └── storage/faiss_agentic/ # LangGraph/biking/nutrition vector database
│   ├── langgraph_chat_workflow/   # LangGraph chatbot
│   └── crewai_workflow/           # CrewAI multi-agent policy generator
│
├── app/                           # Unified Streamlit portfolio UI
│   ├── main.py                    # Home page
│   ├── pages/                     # One page per pipeline
│   └── components/                # Reusable UI components
│
├── data/
│   └── sample_files/              # PDFs and sample documents
│
├── outputs/                       # Generated workflow diagrams
├── .env                           # API keys (git-ignored)
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Model Configuration

All pipelines use a shared model configuration via `shared/utils/llm_utils.py`. The active model is set in `.env`:

```env
DEFAULT_MODEL=llama-3.3-70b-versatile   # Used by all pipelines
CREWAI_MODEL=groq/llama-3.3-70b-versatile  # CrewAI specific (optional override)
```

To switch models, update `.env` — no code changes required.

---

## Common Issues

**Wrong Python version**
This project requires Python 3.11. Using 3.12 causes HuggingFace dependency conflicts. Always create the venv with `python3.11 -m venv .venv`.

**`ModuleNotFoundError: No module named 'shared'`**
Run `pip install -e .` from the project root with the venv activated.

**Rate limit errors with Groq**
The free tier has token-per-minute limits. CrewAI workflows are particularly token-heavy. Wait 30-60 seconds and retry — the pipeline has built-in retry logic.

**Vector database not found**
Run the setup scripts in step 9 above. Each pipeline needs its own database built before use.

**`.env` not loading**
Make sure `.env` is in the project root (same level as `requirements.txt`).