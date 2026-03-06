"""
Setup script to create vector database for agentic workflow
"""
from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db

import os

# vector database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "storage", "faiss_basic")


def main():
    print("\n" + "="*50)
    print("Setting up Vector Database")
    print("="*50 + "\n")
    
    # Load content - you can change this URL or use a local PDF
    content_path = "https://www.ibm.com/think/topics/agentic-ai"
    
    print("Step 1: Loading content...")
    pages = load_content(content_path)
    
    print("\nStep 2: Creating chunks...")
    chunks = create_chunks(pages, chunk_size=500, chunk_overlap=100)
    
    print("\nStep 3: Creating vector database...")
    db = create_vector_db(chunks, persist_directory=VECTOR_DB_PATH)
    print(f"✓ Database saved to: {VECTOR_DB_PATH}")
    print("\n" + "="*50)
    print("✓ Vector database setup complete!")
    print("="*50)

if __name__ == "__main__":
    main()