# import keys
from dotenv import load_dotenv
import os
load_dotenv()


# import libraries
import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from shared.utils.llm_utils import get_llm, DEFAULT_MODEL

# connect to mcp server
client = MultiServerMCPClient(
    {
        "MCP_Server": {
            "transport": "sse",
            "url": "http://127.0.0.1:8000/sse",
        }
    }
)

# function to get tools from mcp server
async def setup_tools():
    tools = await client.get_tools()
    return tools

async def main():
    tool_list = await setup_tools()
    llm = get_llm(model=DEFAULT_MODEL, temperature=0.1)
    system_prompt = """You are a knowledgeable research assistant with access to these tools:
- web_search: retrieve real-time information from the internet
- search_docs: search the Deloitte company profile PDF
- generate_otp: generate a one-time password only when explicitly requested
Always use a tool to find information. Cite your source when answering."""
    agent = create_react_agent(llm, tools=tool_list, prompt=system_prompt)

    print("Type 'exit', 'quit', or 'q' to quit.\n")

    while True:
        user_question = input("Ask a question: ")

        if user_question.strip().lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        if not user_question.strip():
            print("Please enter a question.")
            continue

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a knowledgeable research assistant. You have access to the following tools and must use them appropriately:

- **search**: Use this to retrieve current, real-time information from the internet. Always use this for questions about recent events, news, or anything that may have changed.
- **search_docs**: Use this to search the Deloitte company profile PDF for internal or specific document-based information. Prefer this over web search when the answer is likely in the document.
- **generate_otp**: Use this only when the user explicitly requests a one-time password or random number.

Guidelines:
- Always use a tool to find information — never guess or rely on prior knowledge.
- If the document search returns relevant results, prefer that over web search.
- If the document search returns insufficient results, supplement with web search.
- Cite your source (document or web) when providing an answer.
- If you cannot find the answer using the available tools, say so clearly.
- When generate_otp returns a number, display it exactly as returned with no additional commentary."""

                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ]
            }
        )

        print(f"\nAnswer: {result['messages'][-1].content}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")