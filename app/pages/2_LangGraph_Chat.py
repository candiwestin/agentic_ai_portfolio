"""
LangGraph Chat Demo - State-managed conversational agent
"""
import streamlit as st
import sys
import os
# Add parent directory (streamlit_app) and project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv
load_dotenv()

from shared.utils.llm_utils import get_llm, invoke_llm

st.set_page_config(page_title="LangGraph Chat", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 3rem; }
    .page-title { 
        font-size: 2.5rem; 
        font-weight: 600; 
        margin-bottom: 0.5rem; 
        background: linear-gradient(135deg, #32CD32 0%, #28a428 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .page-subtitle { font-size: 1.1rem; color: #ffffff; font-weight: 400; margin-bottom: 2rem; }
    .info-box {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(50, 205, 50, 0.1), rgba(40, 164, 40, 0.05));
        border-left: 4px solid #32CD32;
        border-radius: 4px;
        margin: 1.5rem 0;
        color: #ffffff;
    }
    .info-box h4 { color: #32CD32; margin-bottom: 0.5rem; }
    .chat-message { padding: 1rem; margin: 1rem 0; border-radius: 4px; }
    .user-message { background: #1a1a1a; border-left: 3px solid #32CD32; color: #ffffff; }
    .assistant-message { background: #2a2a2a; border: 1px solid #32CD32; color: #ffffff; }
    hr { border: none; border-top: 1px solid #e0e0e0; margin: 2rem 0; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">LangGraph Chat</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Conversational agent with state management</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h4>What This Bot Does</h4>
    <p>This is a general-purpose conversational AI powered by Groq's Llama model. It has:</p>
    <ul>
        <li><strong>No document access</strong> - Uses only its training knowledge</li>
        <li><strong>Conversation memory</strong> - Remembers the full chat history</li>
        <li><strong>Adjustable settings</strong> - Change model and temperature in sidebar</li>
    </ul>
    <h4>What to Ask</h4>
    <p>Try anything general:</p>
    <ul>
        <li>"Explain machine learning in simple terms"</li>
        <li>"What's the difference between AI and ML?"</li>
        <li>"Help me understand recursion"</li>
        <li>"Tell me a programming joke"</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.markdown('<h1 class="page-title">LangGraph Chat</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Conversational agent with state management</p>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Conversation Settings")
    model_choice = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Statistics")
    st.markdown(f"Messages: {len(st.session_state.chat_history)}")
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("### Conversation")

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant</strong><br>{message["content"]}</div>', unsafe_allow_html=True)

user_input = st.text_input("Message", placeholder="Type your message...", label_visibility="collapsed")

if st.button("Send", use_container_width=True) and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking..."):
        try:
            llm = get_llm(model=model_choice, temperature=temperature)
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history]
            response = invoke_llm(llm, messages)
            st.session_state.chat_history.append({"role": "assistant", "content": response.content})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")