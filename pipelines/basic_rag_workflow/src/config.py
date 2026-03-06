"""
Central configuration for Basic RAG Workflow.
All paths and source URLs are defined here — import from this file, never hardcode.
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "storage", "faiss_basic")
VECTOR_DB_PATH_CUSTOM = os.path.join(BASE_DIR, "storage", "faiss_basic_custom")

# Project root (for resolving local PDF paths)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Source documents
SOURCE_URLS = [
    "https://www.ibm.com/think/topics/agentic-ai",
    "https://www.nasa.gov/international-space-station",
    os.path.join(PROJECT_ROOT, "data", "sample_files", "1706.03762v7.pdf"),
]