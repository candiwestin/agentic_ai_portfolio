"""Document loading and indexing for MCP agent workflow"""
import os
from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db
from config import VECTOR_DB_PATH

# project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# PDF path
PDF_PATH = os.path.join(PROJECT_ROOT, "data", "sample_files", "Deloitte_Company_Profile.pdf")


def load_pdf_to_db(file_path=PDF_PATH, persist_directory=VECTOR_DB_PATH):
    """Load PDF and create FAISS index"""
    print(f"Loading: {file_path}")
    pages = load_content(file_path)
    chunks = create_chunks(pages)
    create_vector_db(chunks, persist_directory=persist_directory)
    print(f"✓ Loaded {len(chunks)} chunks from {file_path}")

if __name__ == "__main__":
    load_pdf_to_db()