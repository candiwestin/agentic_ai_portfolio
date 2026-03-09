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
    "https://en.wikipedia.org/wiki/National_Football_League",
    "https://en.wikipedia.org/wiki/2024_NFL_season",
    "https://en.wikipedia.org/wiki/2024%E2%80%9325_NFL_playoffs",
    "https://en.wikipedia.org/wiki/Super_Bowl_LIX",
]