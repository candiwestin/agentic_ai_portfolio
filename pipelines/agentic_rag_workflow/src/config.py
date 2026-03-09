"""
Central configuration for Agentic RAG Workflow.
All paths and source URLs are defined here — import from this file, never hardcode.
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "storage", "faiss_agentic")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Source documents
SOURCE_URLS = [
    os.path.join(PROJECT_ROOT, "data", "sample_files", "mountain_biking_guide.pdf"),
    "https://en.wikipedia.org/wiki/Mountain_bike",
    "https://en.wikipedia.org/wiki/Mountain_bike_racing",
]