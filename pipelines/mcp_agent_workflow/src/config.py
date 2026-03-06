"""
Central configuration for MCP Agent Workflow.
All paths are defined here — import from this file, never hardcode.
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "storage", "faiss_mcp")

# MCP server
MCP_SERVER_URL = "http://127.0.0.1:8000/sse"