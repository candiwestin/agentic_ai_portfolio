"""
RAG (Retrieval-Augmented Generation) Pipeline
This pipeline loads documents (PDF/web), chunks them, creates embeddings,
stores in FAISS vector database, and answers queries using retrieved context.
LLM Provider Options:
- Ollama: Local, free, slower, privacy-friendly
- Groq: Cloud, very fast, generous free tier, good quality
- OpenAI: Cloud, paid, best quality, most reliable
Vector Store Options:
- FAISS: Fast, in-memory, production-ready (current)
- Chroma: Feature-rich, persistent, good for prototyping
"""
import os
from dotenv import load_dotenv
from pipelines.basic_rag_workflow.src.config import VECTOR_DB_PATH, SOURCE_URLS
from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db
from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
from shared.utils.llm_utils import get_llm, DEFAULT_MODEL

load_dotenv()

def query_rag(db, user_input):
    """Query the RAG system and get response"""
    relevant_chunks = retrieve_chunks(db, user_input, k=5)
    final_context = format_chunks(relevant_chunks)
    prompt = f'''
You are an expert in analyzing technical documents. Use the context below to answer the user's question.
The context may include partial information, figure captions, or related text.
Extract and explain whatever relevant information is available, even if incomplete.
If you genuinely find NO relevant information at all, only then say 'no context found'.
User query: {user_input}
Context: {final_context}
Provide a detailed answer based on what's available in the context.
'''
    llm = get_llm(model=DEFAULT_MODEL, temperature=0)
    response = llm.invoke(prompt)
    return response.content

def main():
    # Load the first URL as the single-doc entry point (see setup_multi_docs.py for full index)
    content_path = SOURCE_URLS[0]
    pages = load_content(content_path)
    chunks = create_chunks(pages)
    db = create_vector_db(chunks, persist_directory=VECTOR_DB_PATH)

    print("\n" + "="*50)
    print("RAG System Ready! Ask your questions.")
    print("="*50 + "\n")

    while True:
        user_input = input("\nEnter your query (or 'quit' to exit): ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        print("\nProcessing...")
        response = query_rag(db, user_input)
        print("\n" + "="*50)
        print("RESPONSE:")
        print("="*50)
        print(response)

if __name__ == "__main__":
    main()