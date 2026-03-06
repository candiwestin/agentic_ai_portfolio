# MCP Agent Workflow

A client-server AI agent system built on FastMCP and LangChain. The server exposes tools via the MCP protocol over SSE. The client connects to the server, retrieves the tools, and uses a LangChain agent powered by Groq to answer questions.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## How It Works

The agent has access to three tools exposed by the MCP server:

| Tool | Description |
|------|-------------|
| `search` | Searches the web using Tavily for current information |
| `search_docs` | Searches the Deloitte company profile PDF using FAISS vector search |
| `generate_otp` | Generates a random 6-digit number on request |

The agent automatically decides which tool to use based on your question.

---

## Running the Pipeline

This is a client-server system. **Both processes run simultaneously in separate terminals.**

### Terminal 1 — Start the Server

```bash
source .venv/bin/activate
cd /path/to/agentic_ai_portfolio
python -m pipelines.mcp_agent_workflow.src.mcp.mcp_server
```

Wait for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2 — Start the Client

```bash
source .venv/bin/activate
cd /path/to/agentic_ai_portfolio
python -m pipelines.mcp_agent_workflow.src.agents.agent
```

---

## Sample Questions

### search_docs — Deloitte PDF
```
What services does Deloitte offer?
How many employees does Deloitte have?
What industries does Deloitte serve?
When was Deloitte founded?
```

### search — Web / Tavily
```
What is Deloitte's current revenue?
Who is the current CEO of Deloitte?
What are the latest news stories about Deloitte?
How does Deloitte compare to PwC?
```

### generate_otp
```
Generate a one-time password for me.
I need a 6 digit code.
```

---

## Setting Up the Vector Database

The Deloitte PDF must be indexed before running. Build the database:

```bash
python -m pipelines.mcp_agent_workflow.src.data.load_documents
```

The index is stored at `storage/faiss_mcp`.

---

## Pipeline Structure

```
pipelines/mcp_agent_workflow/
├── src/
│   ├── mcp/
│   │   └── mcp_server.py         # MCP server — Terminal 1
│   ├── agents/
│   │   └── agent.py              # LangChain agent client — Terminal 2
│   └── data/
│       └── load_documents.py     # Document loading and FAISS indexing
└── storage/
    └── faiss_mcp/                # Deloitte PDF vector database
        ├── index.faiss
        └── index.pkl
```

**Shared utilities used:**

```
shared/utils/llm_utils.py         # LLM initialization, DEFAULT_MODEL
shared/utils/loader_utils.py      # PDF loading
shared/utils/chunking_utils.py    # Text splitting
shared/utils/vector_utils.py      # FAISS vector store
```

---

## Common Issues

**Server not running when starting the client**
Always start Terminal 1 first and wait for the Uvicorn message before starting Terminal 2.

**FAISS index not found**
Run: `python -m pipelines.mcp_agent_workflow.src.data.load_documents`

**`ModuleNotFoundError: No module named 'shared'`**
Run `pip install -e .` from the project root with the venv activated.