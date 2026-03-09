"""
Setup script to create vector database for Basic RAG workflow.
Source URLs are defined in config.py — edit there to change documents.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import VECTOR_DB_PATH, SOURCE_URLS
from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db

def main():
    print("\n" + "="*50)
    print("Setting up Basic RAG Vector Database")
    print("="*50 + "\n")

    all_pages = []
    for content_path in SOURCE_URLS:
        print(f"Loading: {content_path}")
        try:
            pages = load_content(content_path)
            all_pages.extend(pages)
            print(f"✓ Loaded {len(pages)} pages")
        except Exception as e:
            print(f"Error loading {content_path}: {e}")
            continue

    print(f"\n✓ Total pages loaded: {len(all_pages)}")
    chunks = create_chunks(all_pages, chunk_size=500, chunk_overlap=100)
    print(f"✓ Created {len(chunks)} chunks")
    create_vector_db(chunks, persist_directory=VECTOR_DB_PATH)
    print(f"✓ Database saved to: {VECTOR_DB_PATH}")
    print("\n" + "="*50)
    print("✓ Basic RAG vector database complete!")
    print("="*50)

if __name__ == "__main__":
    main()