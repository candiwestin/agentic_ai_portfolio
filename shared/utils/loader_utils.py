"""Document loading utilities"""
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader


def load_content(content_path):
    """Load and split content from PDF or web page"""
    print(f"Loading content from: {content_path}")
    
    if content_path.endswith('.pdf'):
        loader = PyPDFLoader(content_path)
    else:
        loader = WebBaseLoader(content_path)
    
    pages = loader.load_and_split()
    print(f"✓ Loaded {len(pages)} pages/sections")
    return pages