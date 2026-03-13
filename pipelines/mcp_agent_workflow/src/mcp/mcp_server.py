# import keys
from dotenv import load_dotenv
import os

load_dotenv()

# import libraries
from fastmcp import FastMCP
from langchain_tavily import TavilySearch 
import random
from shared.utils.vector_utils import load_vector_db
from pipelines.mcp_agent_workflow.src.config import VECTOR_DB_PATH

# create MCP instance
mcp = FastMCP("MCP_Server")

# define search function
@mcp.tool()
def web_search(query:str) -> str:
    """
    tool to search the web for current information using Tavily
    """
    print("web search tool is being called")
    tavily_obj = TavilySearch(max_results=3)
    results = tavily_obj.invoke(query)
    return str(results)

# define random number generation function
@mcp.tool()
def generate_otp() -> str:
    """
    tool to generate a random 6 digit number
    """
    print("generate otp tool is being called")
    otp = random.randint(100000, 999999)
    return str(otp)

# define document search function
@mcp.tool()
def search_docs(query: str) -> str:
    """
    Search the Deloitte company profile PDF for relevant information
    """
    print("search docs tool is being called")
    db = load_vector_db(persist_directory=VECTOR_DB_PATH)
    results = db.similarity_search(query, k=3)
    output = ""
    for r in results:
        output += f"Page: {r.metadata.get('page', '?')}\n{r.page_content}\n\n"
    return output

# start the MCP server
if __name__ == "__main__":
    #mcp.run(transport="sse", port = 8000)
    try:
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        print("\nServer stopped.")

