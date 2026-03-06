"""
Shared Tools: Dynamic research and generation tools for CrewAI agents.
Uses shared utilities for real web search and LLM calls.
"""
from crewai.tools import tool   
from shared.utils.web_search_utils import web_search, format_search_results
from shared.utils.llm_utils import get_llm, invoke_llm

@tool("research_topic")
def research_topic(query: str) -> str:
    """
    Search the web for current information on any topic.
    Use this to research policies, best practices, regulations, or any subject.
    """
    results = web_search(query, max_results=5)
    return format_search_results(results)

@tool("generate_content")
def generate_content(prompt: str) -> str:
    """
    Generate structured content using the LLM.
    Use this tool by passing a 'prompt' parameter (lowercase) with the content description.
    Example: generate_content(prompt="Write a policy section about eligibility")
    """
    llm = get_llm()
    messages = [{"role": "user", "content": prompt}]
    response = invoke_llm(llm, messages)
    return response.content