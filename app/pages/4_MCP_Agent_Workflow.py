"""
MCP Agent Workflow Demo - Client-server AI agent architecture
"""
import streamlit as st
import os
import requests

st.set_page_config(page_title="MCP Agent Workflow", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3rem; }
    .page-title { 
        font-size: 2.5rem; 
        font-weight: 600; 
        margin-bottom: 0.5rem; 
        background: linear-gradient(135deg, #32CD32 0%, #28a428 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .page-subtitle { font-size: 1.1rem; color: #ffffff; font-weight: 400; margin-bottom: 2rem; }
    .info-box {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(50, 205, 50, 0.1), rgba(40, 164, 40, 0.05));
        border-left: 4px solid #32CD32;
        border-radius: 4px;
        margin: 1.5rem 0;
        color: #ffffff;
    }
    .info-box h4 { color: #32CD32; margin-bottom: 0.5rem; }
    .tool-card {
        padding: 1.5rem;
        background: #1a1a1a;
        border: 1px solid #32CD32;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    .tool-card h4 { color: #32CD32; margin-bottom: 0.5rem; }
    .status-online { color: #32CD32; font-weight: 600; }
    .status-offline { color: #ff4444; font-weight: 600; }
    .arch-box {
        padding: 1.5rem;
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 8px;
        font-family: monospace;
        color: #32CD32;
        margin: 1rem 0;
        white-space: pre;
        font-size: 0.85rem;
    }
    .command-box {
        padding: 1rem;
        background: #0a0a0a;
        border-left: 3px solid #32CD32;
        border-radius: 4px;
        font-family: monospace;
        color: #32CD32;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    hr { border: none; border-top: 1px solid #333; margin: 2rem 0; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">MCP Agent Workflow</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Client-server AI agent using FastMCP, SSE, and LangChain tool orchestration</p>', unsafe_allow_html=True)

# Server status check
def check_server():
    try:
        response = requests.get("http://127.0.0.1:8000/sse", timeout=2, stream=True)
        return response.status_code == 200
    except:
        return False

server_running = check_server()

if server_running:
    st.markdown('<p class="status-online">● MCP Server Online</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="status-offline">● MCP Server Offline</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <h4>To run this pipeline</h4>
        <p>This is a client-server system that runs from the command line. Open two terminals:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Terminal 1 — Start the server:**")
    st.markdown('<div class="command-box">source .venv/bin/activate<br>python -m pipelines.mcp_agent_workflow.src.mcp.mcp_server</div>', unsafe_allow_html=True)
    st.markdown("**Terminal 2 — Start the client:**")
    st.markdown('<div class="command-box">source .venv/bin/activate<br>python -m pipelines.mcp_agent_workflow.src.agents.agent</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Architecture diagram
st.markdown("### Architecture")
st.markdown("""
<div class="arch-box">
User Input
    │
    ▼
┌─────────────────────────────────────────┐
│           LangChain Agent               │
│         (Client — Terminal 2)           │
│                                         │
│   Groq LLaMA 3.1 + Tool Selection      │
└──────────────┬──────────────────────────┘
               │  MCP Protocol (SSE)
               │  http://127.0.0.1:8000
               ▼
┌─────────────────────────────────────────┐
│           FastMCP Server                │
│         (Server — Terminal 1)           │
│                                         │
│  ┌──────────┐ ┌──────────┐ ┌────────┐  │
│  │  search  │ │search_doc│ │  otp   │  │
│  │ (Tavily) │ │ (FAISS)  │ │(random)│  │
│  └──────────┘ └──────────┘ └────────┘  │
└─────────────────────────────────────────┘
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Tools section
st.markdown("### Exposed Tools")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="tool-card">
        <h4>search</h4>
        <p>Web search using Tavily API. Routes questions about current events, news, and real-time information to the internet.</p>
        <p><strong>Example:</strong> "Who is the current CEO of Deloitte?"</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tool-card">
        <h4>search_docs</h4>
        <p>FAISS vector similarity search over the Deloitte company profile PDF. Retrieves the top 3 most relevant chunks.</p>
        <p><strong>Example:</strong> "What services does Deloitte offer?"</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="tool-card">
        <h4>generate_otp</h4>
        <p>Generates a random 6-digit one-time password using Python's random module.</p>
        <p><strong>Example:</strong> "Generate a 6 digit OTP for me"</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Why MCP section
st.markdown("### Why MCP?")
st.markdown("""
<div class="info-box">
    <h4>Model Context Protocol</h4>
    <p>MCP is an open protocol that standardizes how AI models connect to external tools and data sources. 
    Instead of hardcoding tool implementations into the agent, MCP separates concerns:</p>
    <ul>
        <li><strong>Server</strong> owns the tools and exposes them over a standard protocol</li>
        <li><strong>Client</strong> discovers tools at runtime and uses them without knowing implementation details</li>
        <li><strong>SSE transport</strong> enables real-time streaming communication between client and server</li>
        <li><strong>Swappable</strong> — swap the server or client independently without changing either side</li>
    </ul>
    <p>This mirrors how production AI systems are increasingly being built — modular, protocol-driven, and decoupled.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Tech stack
st.markdown("### Tech Stack")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("**Server**")
    st.markdown("""
    - FastMCP for tool exposure
    - Uvicorn ASGI server
    - SSE (Server-Sent Events) transport
    - Tavily for web search
    - FAISS for vector search
    - HuggingFace embeddings
    """)

with col2:
    st.markdown("**Client**")
    st.markdown("""
    - LangChain MCP adapters
    - Groq LLaMA 3.1 (8B)
    - MultiServerMCPClient
    - LangGraph agent executor
    - Async/await architecture
    """)