"""Web search utilities"""
import os
from langchain_tavily import TavilySearch


def web_search(query, max_results=3):
    """Search the web using Tavily"""
    search_tool = TavilySearch(max_results=max_results)
    results = search_tool.invoke(query)
    return results

def format_search_results(results):
    """Format search results into readable text"""
    if isinstance(results, list):
        formatted = []
        for result in results:
            if isinstance(result, dict):
                title = result.get('title', 'No title')
                content = result.get('content', result.get('snippet', 'No content'))
                url = result.get('url', '')
                formatted.append(f"**{title}**\n{content}\nSource: {url}")
        return "\n\n".join(formatted)
    return str(results)