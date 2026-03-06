"""
Central configuration for Agentic RAG Workflow.
All paths and source URLs are defined here — import from this file, never hardcode.
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "storage", "faiss_agentic")

# Source documents
SOURCE_URLS = [
    "https://langchain-ai.github.io/langgraph/concepts/why-langgraph/",
    "https://en.wikipedia.org/wiki/Mountain_bike",
    "https://en.wikipedia.org/wiki/Nutrition",
]