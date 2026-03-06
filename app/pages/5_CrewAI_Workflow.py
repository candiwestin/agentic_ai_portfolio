"""
CrewAI Workflow Demo - Multi-agent collaboration showcase
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

st.set_page_config(page_title="CrewAI Workflow", layout="wide")

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
    .agent-card {
        padding: 1.5rem;
        background: #1a1a1a;
        border: 1px solid #32CD32;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #ffffff;
        height: 100%;
    }
    .agent-card h4 { color: #32CD32; margin-bottom: 0.5rem; }
    .agent-number {
        display: inline-block;
        width: 28px;
        height: 28px;
        background: #32CD32;
        color: #000;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-weight: 700;
        margin-right: 8px;
        font-size: 0.85rem;
    }
    .arch-box {
        padding: 1.5rem;
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 8px;
        font-family: monospace;
        color: #32CD32;
        margin: 1rem 0;
        white-space: pre;
        font-size: 0.85rem;
    }
    .command-box {
        padding: 1rem;
        background: #0a0a0a;
        border-left: 3px solid #32CD32;
        border-radius: 4px;
        font-family: monospace;
        color: #32CD32;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    hr { border: none; border-top: 1px solid #333; margin: 2rem 0; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">CrewAI Workflow</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Multi-agent collaboration with role-based sequential task execution</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h4>What This Does</h4>
    <p>Four specialized AI agents collaborate sequentially to produce a complete, compliance-reviewed
    policy document on <strong>any topic you choose</strong>. Each agent has a distinct role, expertise, and
    responsibility — output from one agent feeds directly into the next.</p>
    <p><strong>Use case:</strong> Policy generation with real web research, drafting, compliance review, and final editing —
    fully automated by a crew of LLM agents.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Architecture
st.markdown("### Architecture")
st.markdown("""
<div class="arch-box">
User Request: "Create a parental leave policy for a US startup"
        │
        ▼
┌───────────────────────────────────────────────────────┐
│                    CrewAI Crew                        │
│              Process: Sequential                      │
│                                                       │
│  Agent 1          Agent 2          Agent 3            │
│  HR Analyst  ───► Policy Writer ──► Compliance  ──►  │
│  (Research)       (Draft)           (Review)          │
│                                                       │
│                                        Agent 4        │
│                                        Editor         │
│                                        (Finalize) ──► │
└───────────────────────────────────────────────────────┘
        │
        ▼
Final Policy Document (publication-ready)
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Agents
st.markdown("### The Agents")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="agent-card">
        <h4><span class="agent-number">1</span>Policy Research Analyst</h4>
        <p><strong>Role:</strong> Researcher</p>
        <p><strong>Goal:</strong> Research current best practices, legal requirements, and real examples for any policy topic</p>
        <p><strong>Expertise:</strong> 15 years researching workplace policies, labor laws, and regulatory requirements across industries</p>
        <p><strong>Output:</strong> Comprehensive research points with sources covering all relevant aspects of the topic</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-card">
        <h4><span class="agent-number">3</span>Compliance & Legal Reviewer</h4>
        <p><strong>Role:</strong> Risk reviewer</p>
        <p><strong>Goal:</strong> Identify compliance gaps, legal risks, and security vulnerabilities</p>
        <p><strong>Expertise:</strong> Legal requirements, data protection laws, risk management</p>
        <p><strong>Output:</strong> Detailed compliance review notes with specific required additions</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h4><span class="agent-number">2</span>Policy Writer</h4>
        <p><strong>Role:</strong> Document author</p>
        <p><strong>Goal:</strong> Write clear, structured, actionable policy documents</p>
        <p><strong>Expertise:</strong> Translating research into implementable company policies</p>
        <p><strong>Output:</strong> Complete structured policy document with numbered sections</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-card">
        <h4><span class="agent-number">4</span>Policy Editor & Formatter</h4>
        <p><strong>Role:</strong> Final editor</p>
        <p><strong>Goal:</strong> Produce polished, professional, publication-ready documents</p>
        <p><strong>Expertise:</strong> Consistency, clarity, professional formatting</p>
        <p><strong>Output:</strong> Final formatted policy document ready for distribution</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# How to run
st.markdown("### Run This Pipeline")
st.markdown("**From the project root with your virtual environment activated:**")
st.markdown('<div class="command-box">python -m pipelines.crewai_workflow.src.crewai_version "Create a parental leave policy for a US startup"</div>', unsafe_allow_html=True)
st.markdown("Expected runtime: 2–5 minutes depending on Groq rate limits.")

st.markdown("""
<div class="info-box">
    <h4>Example Topics to Try</h4>
    <ul>
        <li>"Create a parental leave policy for a US startup"</li>
        <li>"Write a remote work policy for a global tech company"</li>
        <li>"Draft a data privacy policy for a healthcare SaaS"</li>
        <li>"Create an AI usage policy for a financial services firm"</li>
        <li>"Write a social media policy for a marketing agency"</li>
    </ul>
    <p>The agents will search the web for current information, draft a structured policy, review it for legal compliance, and produce a final publication-ready document.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Tech stack
st.markdown("### Tech Stack")
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    **Agent Framework**
    - CrewAI 1.9.3
    - Sequential process execution
    - Role-based agent design
    - Context passing between tasks
    """)

with col2:
    st.markdown("""
    **LLM & Tools**
    - Groq LLaMA 3 (via LiteLLM)
    - Tavily web search
    - Dynamic topic input via CLI
    - Built-in rate limit retry logic
    """)