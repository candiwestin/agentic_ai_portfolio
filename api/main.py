from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Agentic AI Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: str
    history: list = []

# ── Health check — keeps Render warm via UptimeRobot ──
@app.get("/health")
@app.post("/health")
@app.head("/health")
def health():
    return {"status": "ok"}

# ── Basic RAG ──
@app.post("/api/basic-rag")
async def basic_rag(request: QueryRequest):
    try:
        from shared.utils.vector_utils import load_vector_db
        from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
        from shared.utils.llm_utils import get_llm, invoke_llm

        db_path = os.path.join(os.path.dirname(__file__), '../pipelines/basic_rag_workflow/storage/faiss_basic')
        vector_db = load_vector_db(persist_directory=db_path)
        chunks = retrieve_chunks(vector_db, request.query, k=5)
        context = format_chunks(chunks)
        llm = get_llm()
        prompt = f"Question: {request.query}\nContext: {context}\n\nProvide a detailed accurate answer."
        response = invoke_llm(llm, [{"role": "user", "content": prompt}])
        sources = [c.page_content[:200] for c in chunks[:3]]
        return {"answer": response.content, "sources": sources}
    except Exception as e:
        return {"error": str(e)}

# ── LangGraph Chat ──
@app.post("/api/langgraph-chat")
async def langgraph_chat(request: ChatRequest):
    try:
        from shared.utils.llm_utils import get_llm, invoke_llm

        llm = get_llm()
        messages = request.history + [{"role": "user", "content": request.message}]
        response = invoke_llm(llm, messages)
        return {"response": response.content}
    except Exception as e:
        return {"error": str(e)}

# ── Agentic RAG ──
@app.post("/api/agentic-rag")
async def agentic_rag(request: QueryRequest):
    try:
        from pydantic import BaseModel as PydanticBase, Field
        from typing import Literal
        from shared.utils.vector_utils import load_vector_db
        from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
        from shared.utils.llm_utils import get_llm, invoke_llm
        from shared.utils.web_search_utils import web_search, format_search_results

        class Router(PydanticBase):
            route: Literal["vector_db", "web_search", "generic"]= Field(description="Route the query")

        llm = get_llm()
        classifier = llm.with_structured_output(Router)
        system = "Classify to 'vector_db', 'web_search', or 'generic'. vector_db for AI/ML/tech topics, web_search for current events, generic for simple questions."
        routing = classifier.invoke([{"role": "system", "content": system}, {"role": "user", "content": request.query}])
        route = routing.route

        if route == "vector_db":
            db_path = os.path.join(os.path.dirname(__file__), '../pipelines/agentic_rag_workflow/storage/faiss_agentic')
            vector_db = load_vector_db(persist_directory=db_path)
            chunks = retrieve_chunks(vector_db, request.query, k=5)
            context = format_chunks(chunks)
        elif route == "web_search":
            results = web_search(request.query, max_results=3)
            context = format_search_results(results)
        else:
            context = "Use your general knowledge."

        response = invoke_llm(llm, [{"role": "user", "content": f"Question: {request.query}\nContext: {context}\n\nAnswer clearly."}])
        return {"answer": response.content, "route": route}
    except Exception as e:
        return {"error": str(e)}
