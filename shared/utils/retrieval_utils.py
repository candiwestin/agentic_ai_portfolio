"""Retrieval utilities"""


def retrieve_chunks(vector_db, query, k=5):
    """Retrieve relevant chunks from vector database"""
    retriever = vector_db.as_retriever(search_kwargs={"k": k})
    relevant_chunks = retriever.invoke(query)
    return relevant_chunks


def format_chunks(chunks):
    """Format chunks into a single context string"""
    return "\n\n".join([chunk.page_content for chunk in chunks])