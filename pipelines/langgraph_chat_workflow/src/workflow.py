"""
Simple LangGraph Chatbot Workflow

LLM Provider Options:
- Ollama: Local, free, slower, privacy-friendly
- Groq: Cloud, very fast, generous free tier, good quality
- OpenAI: Cloud, paid, best quality, most reliable

To switch: Comment/uncomment the llm = ... section in llm_call()
Make sure corresponding API key is in .env file
"""

# import necessary packages for langgraph and state machine implementation
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
# from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI
from langgraph.graph.message import Messages, add_messages
from shared.utils.llm_utils import get_llm, DEFAULT_MODEL
from dotenv import load_dotenv

# Import our utility functions
from shared.utils.graph_utils import generate_graph_visualization

# Load environment variables
load_dotenv()

# create state machine
class State(TypedDict):
    messages: Annotated[list[Messages], add_messages]

# create state graph
graph_builder = StateGraph(State)

def llm_call(state: State):
    user_input = state["messages"]
    
    # Option 1: Ollama (local, free)
    # llm = ChatOllama(model="llama3.2", temperature=0)
    
    # Option 2: Groq (cloud, fast, free tier) - CURRENT
    llm = get_llm(model=DEFAULT_MODEL, temperature=0)
    
    # Option 3: OpenAI (cloud, paid, best quality)
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    llm_response = llm.invoke(user_input)
    return {"messages": [llm_response]}

# build the graph. This is the workflow. Add nodes and edges to the graph.
graph_builder.add_node("chatbot", llm_call)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# compile the graph. This is the workflow.
workflow = graph_builder.compile()

# Generate graph visualization (production-ready, reusable). 
generate_graph_visualization(
    workflow,
    graph_file="outputs/basic_workflow_diagram.png",
    hash_file="outputs/basic_workflow_diagram.hash"
)

# Execute the workflow
while True:
    user_input = input("Enter your question: ")
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        break
    result = workflow.invoke({"messages": [{"role": "user", "content": user_input}]})
    response = result["messages"][-1].content
    print("\nResponse:", response)