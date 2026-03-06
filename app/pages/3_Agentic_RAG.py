"""
Agentic RAG Demo - Intelligent routing system
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv
load_dotenv()

# Import config from pipeline — single source of truth for paths and URLs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipelines/agentic_rag_workflow/src')))
from config import VECTOR_DB_PATH, SOURCE_URLS

from typing import Literal
from pydantic import BaseModel, Field
from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db, load_vector_db
from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
from shared.utils.llm_utils import get_llm, invoke_llm
from shared.utils.web_search_utils import web_search, format_search_results

st.set_page_config(page_title="Agentic RAG", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3rem; }
    .page-title {
        font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #32CD32 0%, #28a428 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .page-subtitle { font-size: 1.1rem; color: #ffffff; font-weight: 400; margin-bottom: 2rem; }
    .info-box {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(50,205,50,0.1), rgba(40,164,40,0.05));
        border-left: 4px solid #32CD32; border-radius: 4px; margin: 1.5rem 0; color: #ffffff;
    }
    .info-box h4 { color: #32CD32; margin-bottom: 0.5rem; }
    .route-indicator { display: inline-block; padding: 0.5rem 1rem; border-radius: 4px; font-weight: 600; font-size: 0.9rem; margin: 0.5rem 0; }
    .route-vectordb { background: #32CD32; color: #1a1a1a; }
    .route-websearch { background: #28a428; color: #ffffff; }
    .route-generic { background: #90EE90; color: #1a1a1a; }
    .chat-message { padding: 1rem; margin: 1rem 0; border-radius: 4px; }
    .user-message { background: #1a1a1a; border-left: 3px solid #32CD32; color: #ffffff; }
    .assistant-message { background: #2a2a2a; border: 1px solid #32CD32; color: #ffffff; }
    hr { border: none; border-top: 1px solid #e0e0e0; margin: 2rem 0; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">Agentic RAG</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Intelligent routing between vector search, web search, and direct responses</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h4>How This Works</h4>
    <p>This intelligent system automatically routes your question to the best source:</p>
    <ul>
        <li><strong>Vector DB (Green)</strong> - Searches loaded documents (LangGraph docs, Mountain Biking Wikipedia, Nutrition Wikipedia)</li>
        <li><strong>Web Search (Dark Green)</strong> - Searches the internet for current information</li>
        <li><strong>Generic (Light Green)</strong> - Uses LLM's general knowledge</li>
    </ul>
    <h4>What to Ask</h4>
    <ul>
        <li><strong>Document:</strong> "Why use LangGraph?" or "What are the types of mountain bikes?" (routes to Vector DB)</li>
        <li><strong>Document:</strong> "What are macronutrients?" or "What is protein used for in the body?" (routes to Vector DB)</li>
        <li><strong>Current:</strong> "What is the latest news in AI today?" (routes to Web Search)</li>
        <li><strong>General:</strong> "What is 5 + 5?" (routes to Generic)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

class MessageClassifier(BaseModel):
    message_type: Literal["vector_db", "web_search", "generic_search"] = Field(description="Classify user input")

if 'agentic_chat_history' not in st.session_state:
    st.session_state.agentic_chat_history = []
if 'agentic_vector_db' not in st.session_state:
    st.session_state.agentic_vector_db = None
if 'agentic_db_loaded' not in st.session_state:
    st.session_state.agentic_db_loaded = False

def build_index():
    """Build FAISS index from source URLs."""
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    all_chunks = []
    for url in SOURCE_URLS:
        try:
            pages = load_content(url)
            chunks = create_chunks(pages)
            all_chunks.extend(chunks)
        except Exception as e:
            st.warning(f"Could not load {url}: {e}")
    if all_chunks:
        return create_vector_db(all_chunks, persist_directory=VECTOR_DB_PATH)
    return None

def get_vector_db():
    """Load existing index or build it on first run."""
    index_file = os.path.join(VECTOR_DB_PATH, "index.faiss")
    if os.path.exists(index_file):
        return load_vector_db(persist_directory=VECTOR_DB_PATH)
    return build_index()

with st.sidebar:
    st.markdown("### System Setup")
    if st.button("Load Vector Database", use_container_width=True):
        with st.spinner("Loading database (building index if first run — this may take a minute)..."):
            try:
                st.session_state.agentic_vector_db = get_vector_db()
                st.session_state.agentic_db_loaded = True
                st.success("Database ready")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Routing Logic")
    st.markdown("**Vector DB** - Technical questions, document queries")
    st.markdown("**Web Search** - Current events, real-time data")
    st.markdown("**Generic** - Simple questions, basic definitions")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Statistics")
    st.markdown(f"Exchanges: {len(st.session_state.agentic_chat_history)}")
    if st.button("Clear History", use_container_width=True):
        st.session_state.agentic_chat_history = []
        st.rerun()

if not st.session_state.agentic_db_loaded:
    st.markdown("Click **Load Vector Database** in the sidebar to begin. The index will build automatically on first run — web search and generic responses are always available once loaded.")
else:
    st.markdown("### Conversation")

    for exchange in st.session_state.agentic_chat_history:
        st.markdown(f'<div class="chat-message user-message">{exchange["question"]}</div>', unsafe_allow_html=True)
        route = exchange["route"]
        route_class = f"route-{route.replace('_', '')}"
        route_label = route.replace('_', ' ').title()
        st.markdown(f'<span class="route-indicator {route_class}">Route: {route_label}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-message assistant-message">{exchange["answer"]}</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

    user_query = st.text_input("Question", placeholder="Ask anything...", label_visibility="collapsed")

    if st.button("Submit", use_container_width=True) and user_query:
        with st.spinner("Processing..."):
            try:
                llm = get_llm()
                classifier_llm = llm.with_structured_output(MessageClassifier)

                system_prompt = """Classify user message to 'vector_db', 'web_search', or 'generic_search':
- vector_db: Technical questions, AI/ML topics, document queries
- web_search: Current events, news, real-time information
- generic_search: Simple questions, basic math, definitions"""

                route_messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}]
                routing = classifier_llm.invoke(route_messages)
                route = routing.message_type

                if route == "vector_db" and st.session_state.agentic_vector_db:
                    chunks = retrieve_chunks(st.session_state.agentic_vector_db, user_query, k=5)
                    context = format_chunks(chunks)
                elif route == "web_search":
                    results = web_search(user_query, max_results=3)
                    context = format_search_results(results)
                else:
                    context = "Use your general knowledge to answer."

                final_prompt = f"Question: {user_query}\nContext: {context}\n\nProvide a clear, accurate answer."
                messages = [{"role": "user", "content": final_prompt}]
                response = invoke_llm(llm, messages)

                st.session_state.agentic_chat_history.append({"question": user_query, "answer": response.content, "route": route})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")