"""Text chunking utilities"""
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(pages, chunk_size=500, chunk_overlap=100):
    """Split pages into smaller chunks"""
    print("Creating chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(pages)
    print(f"✓ Created {len(chunks)} chunks")
    return chunks