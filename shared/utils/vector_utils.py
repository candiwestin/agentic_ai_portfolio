"""Vector database utilities"""
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os


def get_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Get embedding model"""
    return HuggingFaceEmbeddings(model_name=model_name)


def create_vector_db(chunks, embeddings=None, persist_directory=None):
    """Create FAISS vector database with embeddings"""
    if persist_directory is None:
        raise ValueError("persist_directory must be specified")
    print("Creating embeddings and vector database...")
    
    if embeddings is None:
        embeddings = get_embeddings()
    
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(persist_directory)
    print("✓ Vector database created and saved")
    return db


def load_vector_db(persist_directory=None, embeddings=None):
    """Load existing FAISS vector database"""
    if persist_directory is None:
        raise ValueError("persist_directory must be specified")
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(f"Vector DB not found at {persist_directory}")

    if embeddings is None:
        embeddings = get_embeddings()
    
    db = FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)
    print("✓ Vector database loaded")
    return db