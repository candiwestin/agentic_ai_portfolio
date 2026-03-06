"""
Basic RAG Demo - Document retrieval and question answering
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv
load_dotenv()

# Import config from pipeline — single source of truth for paths and URLs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipelines/basic_rag_workflow/src')))
from config import VECTOR_DB_PATH, VECTOR_DB_PATH_CUSTOM, SOURCE_URLS

from shared.utils.loader_utils import load_content
from shared.utils.chunking_utils import create_chunks
from shared.utils.vector_utils import create_vector_db, load_vector_db
from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
from shared.utils.llm_utils import get_llm, invoke_llm

st.set_page_config(page_title="Basic RAG", layout="wide")

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
    .chat-message { padding: 1rem; margin: 1rem 0; border-radius: 4px; }
    .user-message { background: #1a1a1a; border-left: 3px solid #32CD32; color: #ffffff; }
    .assistant-message { background: #2a2a2a; border: 1px solid #32CD32; color: #ffffff; }
    .status-box { padding: 1rem; background: #1a1a1a; border-left: 3px solid #32CD32; margin: 1rem 0; color: #ffffff; }
    .chunk-preview { background: #fafafa; padding: 1rem; border-radius: 4px; font-size: 0.9rem; color: #666; margin: 0.5rem 0; }
    hr { border: none; border-top: 1px solid #e0e0e0; margin: 2rem 0; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">Basic RAG</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Document retrieval with contextual question answering</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h4>What's Loaded</h4>
    <p>This system has access to:</p>
    <ul>
        <li><strong>IBM Agentic AI Article</strong> - Concepts, definitions, and use cases</li>
        <li><strong>NASA Space Station Page</strong> - ISS information, missions, and facts</li>
        <li><strong>Attention Is All You Need Paper</strong> - Transformer architecture, multi-head attention</li>
    </ul>
    <h4>What to Ask</h4>
    <ul>
        <li>"What is agentic AI?"</li>
        <li>"Tell me about the International Space Station"</li>
        <li>"Explain the transformer architecture"</li>
        <li>"What is scaled dot-product attention?"</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

if 'rag_vector_db' not in st.session_state:
    st.session_state.rag_vector_db = None
if 'rag_chat_history' not in st.session_state:
    st.session_state.rag_chat_history = []
if 'rag_db_loaded' not in st.session_state:
    st.session_state.rag_db_loaded = False

def build_index():
    """Build FAISS index from source URLs — skips local PDF paths that won't exist on Streamlit Cloud."""
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    all_chunks = []
    for url in SOURCE_URLS:
        if not url.startswith("http"):
            continue  # Skip local PDF paths on Streamlit Cloud
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
    st.markdown("### Document Management")
    doc_option = st.radio("Document source", ["Pre-loaded documents", "Custom URL"], label_visibility="collapsed")

    if doc_option == "Custom URL":
        custom_url = st.text_input("URL or file path")
        if st.button("Load Document", use_container_width=True):
            if custom_url:
                with st.spinner("Processing document..."):
                    try:
                        pages = load_content(custom_url)
                        chunks = create_chunks(pages)
                        st.session_state.rag_vector_db = create_vector_db(chunks, persist_directory=VECTOR_DB_PATH_CUSTOM)
                        st.session_state.rag_db_loaded = True
                        st.success("Document loaded successfully")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        if st.button("Load Pre-loaded Database", use_container_width=True):
            with st.spinner("Loading database (building index if first run — this may take a minute)..."):
                try:
                    st.session_state.rag_vector_db = get_vector_db()
                    st.session_state.rag_db_loaded = True
                    st.success("Database ready")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.session_state.rag_db_loaded:
        st.markdown("**Status**")
        st.markdown("Vector database ready")
        st.markdown(f"Chat history: {len(st.session_state.rag_chat_history)} exchanges")
    if st.button("Clear History", use_container_width=True):
        st.session_state.rag_chat_history = []
        st.rerun()

if not st.session_state.rag_db_loaded:
    st.markdown('<div class="status-box"><strong>Getting Started</strong><br>Click "Load Pre-loaded Database" in the sidebar to begin. The index will build automatically on first run.</div>', unsafe_allow_html=True)
else:
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("### Conversation")
        for exchange in st.session_state.rag_chat_history:
            st.markdown("**Question**")
            st.markdown(exchange["question"])
            st.markdown("**Answer**")
            st.markdown(exchange["answer"])
            st.markdown("<hr>", unsafe_allow_html=True)

        user_query = st.text_input("Ask a question", placeholder="What would you like to know?", label_visibility="collapsed")
        if st.button("Submit", use_container_width=True) and user_query:
            with st.spinner("Processing..."):
                try:
                    relevant_chunks = retrieve_chunks(st.session_state.rag_vector_db, user_query, k=5)
                    context = format_chunks(relevant_chunks)
                    llm = get_llm()
                    prompt = f"""You are an expert in analyzing documents. Use the context below to answer the question.

Question: {user_query}
Context: {context}

Provide a detailed, accurate answer based on the context."""
                    messages = [{"role": "user", "content": prompt}]
                    response = invoke_llm(llm, messages)
                    st.session_state.rag_chat_history.append({"question": user_query, "answer": response.content, "chunks": relevant_chunks})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col2:
        st.markdown("### Retrieved Context")
        if st.session_state.rag_chat_history:
            latest = st.session_state.rag_chat_history[-1]
            st.markdown("**Most relevant passages**")
            for i, chunk in enumerate(latest.get("chunks", [])[:3], 1):
                st.markdown(f"**Source {i}**")
                st.markdown(f'<div class="chunk-preview">{chunk.page_content[:250]}...</div>', unsafe_allow_html=True)
        else:
            st.markdown("Retrieved passages will appear here.")