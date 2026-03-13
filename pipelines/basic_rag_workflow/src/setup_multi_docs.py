"""
Setup script to create vector database from multiple documents.
Source URLs are defined in config.py — edit there to change documents.
"""
import os
from pipelines.basic_rag_workflow.src.config import VECTOR_DB_PATH, SOURCE_URLS
from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db

def load_multiple_documents(content_paths):
    """Load multiple documents and combine them"""
    all_pages = []
    for content_path in content_paths:
        print(f"\nLoading: {content_path}")
        try:
            pages = load_content(content_path)
            all_pages.extend(pages)
            print(f"✓ Loaded {len(pages)} pages")
        except Exception as e:
            print(f"Error loading {content_path}: {e}")
            continue
    return all_pages

def main():
    print("\n" + "="*50)
    print("Setting up Multi-Document Vector Database")
    print("="*50 + "\n")

    print(f"Loading {len(SOURCE_URLS)} document(s)...")
    all_pages = load_multiple_documents(SOURCE_URLS)
    print(f"\n✓ Total pages loaded: {len(all_pages)}")

    print("\n✓ Creating chunks...")
    chunks = create_chunks(all_pages, chunk_size=500, chunk_overlap=100)

    print("\n✓ Creating vector database...")
    db = create_vector_db(chunks, persist_directory=VECTOR_DB_PATH)
    print(f"✓ Database saved to: {VECTOR_DB_PATH}")

    print("\n" + "="*50)
    print("✓ Multi-document vector database complete!")
    print(f"✓ Total chunks: {len(chunks)}")
    print("="*50)

if __name__ == "__main__":
    main()