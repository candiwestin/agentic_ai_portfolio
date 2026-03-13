"""Document loading and indexing for MCP agent workflow"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.mcp_agent_workflow.src.config import VECTOR_DB_PATH
from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db
from pipelines.mcp_agent_workflow.src.config import VECTOR_DB_PATH

SOURCE_URLS = [
    "https://modelcontextprotocol.io/introduction",
    "https://modelcontextprotocol.io/docs/concepts/architecture",
    "https://modelcontextprotocol.io/docs/concepts/tools",
    "https://en.wikipedia.org/wiki/Model_Context_Protocol",
]

def load_documents_to_db(persist_directory=VECTOR_DB_PATH):
    """Load MCP documentation URLs and create FAISS index"""
    all_pages = []
    for url in SOURCE_URLS:
        print(f"Loading: {url}")
        try:
            pages = load_content(url)
            all_pages.extend(pages)
            print(f"✓ Loaded {len(pages)} pages")
        except Exception as e:
            print(f"Error loading {url}: {e}")
            continue
    chunks = create_chunks(all_pages)
    create_vector_db(chunks, persist_directory=persist_directory)
    print(f"✓ Loaded {len(chunks)} chunks into vector DB")

if __name__ == "__main__":
    load_documents_to_db()