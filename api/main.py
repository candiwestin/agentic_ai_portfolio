from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import threading

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

# ── DB state ──
app.state.basic_db = None
app.state.agentic_db = None
app.state.dbs_loaded = False

def load_dbs():
    try:
        from shared.utils.vector_utils import load_vector_db
        basic_path = os.path.join(os.path.dirname(__file__), '../pipelines/basic_rag_workflow/storage/faiss_basic')
        app.state.basic_db = load_vector_db(persist_directory=basic_path)
        print("✓ Basic RAG DB loaded")
    except Exception as e:
        print(f"Basic RAG DB error: {e}")

    try:
        from shared.utils.vector_utils import load_vector_db
        agentic_path = os.path.join(os.path.dirname(__file__), '../pipelines/agentic_rag_workflow/storage/faiss_agentic')
        app.state.agentic_db = load_vector_db(persist_directory=agentic_path)
        print("✓ Agentic RAG DB loaded")
    except Exception as e:
        print(f"Agentic RAG DB error: {e}")

    app.state.dbs_loaded = True
    print("✓ All DBs ready")

@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=load_dbs, daemon=True)
    thread.start()

class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: str
    history: list = []

# ── Health check ──
@app.get("/health")
@app.post("/health")
@app.head("/health")
def health():
    return {"status": "ok", "dbs_loaded": app.state.dbs_loaded}

# ── Basic RAG ──
@app.post("/api/basic-rag")
async def basic_rag(request: QueryRequest):
    try:
        if not app.state.dbs_loaded:
            return {"error": "Vector DBs are still loading, please try again in 30 seconds"}

        from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
        from shared.utils.llm_utils import get_llm, invoke_llm

        vector_db = app.state.basic_db
        if vector_db is None:
            return {"error": "Basic RAG vector DB not available"}

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
        if not app.state.dbs_loaded:
            return {"error": "Vector DBs are still loading, please try again in 30 seconds"}

        from pydantic import BaseModel as PydanticBase, Field
        from typing import Literal
        from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
        from shared.utils.llm_utils import get_llm, invoke_llm
        from shared.utils.web_search_utils import web_search, format_search_results

        class Router(PydanticBase):
            route: Literal["vector_db", "web_search", "generic"] = Field(description="Route the query")

        llm = get_llm()
        classifier = llm.with_structured_output(Router)
        system = "Classify to 'vector_db', 'web_search', or 'generic'. vector_db for mountain biking topics, web_search for current events/news, generic for simple questions."
        routing = classifier.invoke([{"role": "system", "content": system}, {"role": "user", "content": request.query}])
        route = routing.route

        if route == "vector_db":
            vector_db = app.state.agentic_db
            if vector_db is None:
                return {"error": "Agentic RAG vector DB not available"}
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
