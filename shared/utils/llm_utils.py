"""LLM utilities"""
import os
from langchain_groq import ChatGroq

# set a default model and temperature
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")

def get_llm(model=DEFAULT_MODEL, temperature=0):
    """Get configured LLM instance"""
    return ChatGroq(
        model=model,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
        timeout=30
    )


def invoke_llm(llm, messages):
    """Invoke LLM with messages"""
    return llm.invoke(messages)