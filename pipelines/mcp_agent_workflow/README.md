# MCP Agent Workflow

A client-server AI agent system built on FastMCP and LangChain. The server exposes tools via the Model Context Protocol (MCP) over SSE. The client connects to the server, retrieves the available tools, and uses a LangChain agent powered by Groq to answer questions by selecting and invoking the appropriate tool.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## How It Works

```
┌─────────────────────────────┐         ┌─────────────────────────────┐
│        MCP Client           │◄──SSE──►│        MCP Server           │
│   LangChain + Groq agent    │         │   FastMCP tool definitions  │
│   Discovers tools at runtime│         │   Exposes 3 tools via HTTP  │
└─────────────────────────────┘         └─────────────────────────────┘
```

The agent has access to three tools exposed by the MCP server:

| Tool | Description |
|------|-------------|
| `search` | Searches the web using Tavily for current information |
| `search_docs` | Searches the MCP documentation knowledge base using FAISS vector search |
| `generate_otp` | Generates a random 6-digit number on request |

The agent automatically decides which tool to use based on the query — no hardcoded routing logic.

---

## Knowledge Base

The vector database (`storage/faiss_mcp`) contains **149 chunks** sourced from:

| Source | Content |
|--------|---------|
| modelcontextprotocol.io — Introduction | What MCP is, why it exists, core concepts |
| modelcontextprotocol.io — Architecture | Client-server model, transports, message flow |
| modelcontextprotocol.io — Tools | Tool definitions, schemas, invocation patterns |
| Wikipedia — Model Context Protocol | Overview, adoption, ecosystem |

---

## Running the Pipeline

This is a client-server system. **Both processes must run simultaneously in separate terminals.**

### Terminal 1 — Start the MCP Server

```bash
source .venv/bin/activate
python -m pipelines.mcp_agent_workflow.src.mcp.mcp_server
```

Wait for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2 — Start the Client

```bash
source .venv/bin/activate
python -m pipelines.mcp_agent_workflow.src.agents.agent
```

---

## Sample Questions

### Routes to search_docs — MCP knowledge base
```
What is the Model Context Protocol?
How does MCP client-server architecture work?
What are MCP tools and how are they defined?
Why was MCP created?
How does MCP compare to traditional API integrations?
```

### Routes to search — Tavily web search
```
What companies have adopted MCP?
What are the latest MCP developments?
Which AI assistants support MCP?
```

### Routes to generate_otp
```
Generate a one-time password for me.
I need a 6-digit code.
```

---

## Rebuilding the Vector Database

```bash
python -m pipelines.mcp_agent_workflow.src.data.load_documents
```

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
    └── faiss_mcp/                # MCP documentation vector database
        ├── index.faiss
        └── index.pkl
```

**Shared utilities used:**
```
shared/utils/llm_utils.py         # LLM initialization
shared/utils/loader_utils.py      # Web document loading
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