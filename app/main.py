"""
RAG & Agentic AI Portfolio Demo
Clean, professional interface showcasing AI system architectures
"""
import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="AI Systems Portfolio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Simplified Matrix effect
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        position: relative;
        z-index: 10;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 300;
        letter-spacing: -0.02em;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #32CD32 0%, #28a428 50%, #1a1a1a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        color: #ffffff;
        margin-bottom: 3rem;
        line-height: 1.6;
    }
        
    .feature-card {
        padding: 2.5rem;
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #32CD32;
        box-shadow: 0 4px 20px rgba(50, 205, 50, 0.15);
        transform: translateY(-2px);
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: #1a1a1a;
    }
    
    .feature-description {
        font-size: 1rem;
        line-height: 1.6;
        color: #666;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 600;
        margin: 3rem 0 1.5rem 0;
        color: #1a1a1a;
        border-left: 4px solid #32CD32;
        padding-left: 1rem;
    }
    
    .tech-list {
        list-style: none;
        padding: 0;
    }
    
    .tech-list li {
        padding: 0.5rem 0;
        color: #ffffff;
        font-size: 1rem;
        font-weight: 500;
        border-left: 2px solid #32CD32;
        padding-left: 1rem;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }
    
    .tech-list li:hover {
        border-left: 3px solid #32CD32;
        padding-left: 1.2rem;
    }
    
    hr {
        border: none;
        border-top: 2px solid #f0f0f0;
        margin: 3rem 0;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #32CD32 0%, #28a428 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #28a428 0%, #32CD32 100%);
        box-shadow: 0 4px 12px rgba(50, 205, 50, 0.4);
        transform: translateY(-1px);
    }

    .page-subtitle {
        font-size: 1.1rem;
        color: #ffffff;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Matrix effect injected after CSS
st.markdown("""
<iframe id="matrix-frame" style="
    position: fixed;
    top: 0;
    right: 0;
    width: 200px;
    height: 100vh;
    border: none;
    z-index: 0;
    pointer-events: none;
    background: black;
" srcdoc='
<html>
<body style="margin:0;padding:0;background:black;overflow:hidden;">
<canvas id="c"></canvas>
<script>
var c=document.getElementById("c");
var ctx=c.getContext("2d");
c.height=window.innerHeight;
c.width=200;
var chars="01";
var font_size=16;
var columns=c.width/font_size;
var drops=[];
for(var x=0;x<columns;x++)drops[x]=1;
function draw(){
    ctx.fillStyle="rgba(0,0,0,0.05)";
    ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle="#32CD32";
    ctx.font=font_size+"px monospace";
    for(var i=0;i<drops.length;i++){
        var text=chars[Math.floor(Math.random()*chars.length)];
        ctx.fillText(text,i*font_size,drops[i]*font_size);
        if(drops[i]*font_size>c.height&&Math.random()>0.975)drops[i]=0;
        drops[i]++;
    }
}
setInterval(draw,50);
</script>
</body>
</html>
'></iframe>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<h1 class="hero-title">AI Systems Portfolio</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Production-ready implementations showcasing retrieval-augmented generation, '
    'state management, and intelligent routing architectures.</p>', 
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3 class="feature-title">Basic RAG</h3>
        <p class="feature-description">
            Document processing pipeline with vector similarity search. 
            Load documents, create embeddings, and query with contextual responses.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3 class="feature-title">LangGraph Chat</h3>
        <p class="feature-description">
            State-managed conversational agent using graph-based workflows. 
            Clean architecture for complex dialogue systems.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3 class="feature-title">Agentic RAG</h3>
        <p class="feature-description">
            Intelligent routing system that dynamically selects between vector search, 
            web search, or direct LLM responses.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Technical Details
st.markdown('<h2 class="section-header">Technical Implementation</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("**Architecture**")
    st.markdown("""
    <ul class="tech-list">
        <li>LangChain for document processing</li>
        <li>LangGraph for state machines</li>
        <li>FAISS for vector similarity</li>
        <li>Modular utility architecture</li>
    </ul>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("**Models & APIs**")
    st.markdown("""
    <ul class="tech-list">
        <li>Llama 3.3 (70B) via Groq</li>
        <li>HuggingFace embeddings</li>
        <li>Tavily web search</li>
        <li>Pydantic for validation</li>
    </ul>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Usage
st.markdown('<h2 class="section-header">Getting Started</h2>', unsafe_allow_html=True)
st.markdown("""
Select a demo from the sidebar to begin. Each implementation showcases different approaches 
to building production-ready AI systems with clean, maintainable code.
""")

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    st.markdown("Select a demo to explore:")
    st.markdown("")
    st.markdown("**Basic RAG**")
    st.markdown("Traditional document retrieval")
    st.markdown("")
    st.markdown("**LangGraph Chat**")
    st.markdown("Conversational workflows")
    st.markdown("")
    st.markdown("**Agentic RAG**")
    st.markdown("Intelligent routing")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("### About")
    st.markdown("""
    Portfolio demonstration of AI engineering concepts with focus on 
    production-ready architecture and clean code practices.
    """)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("**Candi Westin**")
    st.markdown("Senior Data\AI Engineer")

    # Matrix rain effect (at end of file, after sidebar)
matrix_code = """
<div id="matrix-bg" style="position: fixed; top: 0; right: 0; width: 200px; height: 100vh; background: #000; z-index: -1;"></div>
<canvas id="matrix" style="position: fixed; top: 0; right: 0; width: 200px; height: 100vh; z-index: -1;"></canvas>
<script>
const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');
canvas.width = 200;
canvas.height = window.innerHeight;

const chars = '01';
const fontSize = 16;
const columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#32CD32';
    ctx.font = fontSize + 'px monospace';
    
    for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}
setInterval(draw, 50);
</script>
"""

st.components.v1.html(matrix_code, height=0)