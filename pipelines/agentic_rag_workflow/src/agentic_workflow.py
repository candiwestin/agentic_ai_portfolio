"""
Agentic RAG Workflow with Router
Routes queries to: Vector DB, Web Search, or Generic LLM
"""
import os
from typing import Annotated, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from pipelines.agentic_rag_workflow.src.config import VECTOR_DB_PATH
from shared.utils.llm_utils import DEFAULT_MODEL
from shared.utils.vector_utils import load_vector_db
from shared.utils.retrieval_utils import retrieve_chunks, format_chunks
from shared.utils.llm_utils import get_llm, invoke_llm
from shared.utils.web_search_utils import web_search, format_search_results
from shared.utils.graph_utils import generate_graph_visualization

load_dotenv()

# Pydantic model for routing classification
class MessageClassifier(BaseModel):
    message_type: Literal["vector_db", "web_search", "generic_search"] = Field(
        description="Classify user input to vector_db, web_search, or generic_search"
    )

# State definition
class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_input: str
    message_type: str
    conversation_history: list

# Initialize LLM (shared across nodes)
llm = get_llm(model=DEFAULT_MODEL, temperature=0.1)

# Node 1: Router
def router_node(state: State):
    """Route user query to appropriate handler"""
    user_input = state["messages"][-1]["content"] if isinstance(state["messages"][-1], dict) else state["messages"][-1].content

    classifier_llm = llm.with_structured_output(MessageClassifier)

    system_prompt = f'''
Classify user message to 'vector_db', 'web_search', or 'generic_search' based on these criteria:
- 'vector_db': PREFER THIS for technical questions about AI, machine learning, transformers, attention mechanisms, neural networks, or any technical/academic topic. Also use for questions about loaded documents or specific information.
- 'web_search': ONLY use for questions explicitly about current events with time indicators like "today", "now", "latest", "current", "2024", weather, sports scores, or breaking news.
- 'generic_search': ONLY use for simple questions like basic math, jokes, greetings, or very basic definitions that don't need technical depth.
When in doubt between vector_db and generic_search, CHOOSE vector_db.
'''

    prompt_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    result = classifier_llm.invoke(prompt_messages)
    print(f"Router decision: {result.message_type}")

    return {
        "messages": [{"role": "assistant", "content": result.message_type}],
        "user_input": user_input,
        "message_type": result.message_type
    }

# Node 2: Vector DB
def vector_db_node(state: State):
    """Retrieve relevant information from vector database"""
    user_input = state["user_input"]
    print(f"Searching vector database for: {user_input}")

    try:
        vector_db = load_vector_db(persist_directory=VECTOR_DB_PATH)
        relevant_chunks = retrieve_chunks(vector_db, user_input, k=5)
        final_context = format_chunks(relevant_chunks)
        return {"messages": [{"role": "assistant", "content": final_context}]}
    except Exception as e:
        error_msg = f"Error accessing vector database: {str(e)}"
        print(f"{error_msg}")
        return {"messages": [{"role": "assistant", "content": error_msg}]}

# Node 3: Web Search
def web_search_node(state: State):
    """Search the web for current information"""
    user_input = state["user_input"]
    print(f"Searching web for: {user_input}")

    try:
        search_results = web_search(user_input, max_results=3)
        formatted_results = format_search_results(search_results)
        return {"messages": [{"role": "assistant", "content": formatted_results}]}
    except Exception as e:
        error_msg = f"Error performing web search: {str(e)}"
        print(f"{error_msg}")
        return {"messages": [{"role": "assistant", "content": error_msg}]}

# Node 4: Generic Search
def generic_search_node(state: State):
    """Generate response using LLM's knowledge"""
    user_input = state["user_input"]
    print(f"Generating generic response for: {user_input}")

    prompt_messages = [
        {"role": "system", "content": "You are a helpful assistant. Generate a clear and concise response to the user's query."},
        {"role": "user", "content": user_input}
    ]

    result = invoke_llm(llm, prompt_messages)
    return {"messages": [{"role": "assistant", "content": result.content}]}

# Node 5: Final Response
def final_response_node(state: State):
    """Generate final polished response with conversation history"""
    user_input = state["user_input"]
    context = state["messages"][-1]["content"] if isinstance(state["messages"][-1], dict) else state["messages"][-1].content
    conversation_history = state.get("conversation_history", [])

    print("Generating final response...")

    history_text = ""
    if conversation_history:
        history_text = "Previous conversation:\n"
        for entry in conversation_history[-3:]:
            history_text += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n\n"

    user_prompt = f"""
{history_text}
Current user query: {user_input}
Retrieved context: {context}

Generate a concise and helpful response that:
1. Takes into account the conversation history above
2. Uses the retrieved context to answer accurately
3. Maintains continuity with previous exchanges

Provide a clear, well-formatted answer.
"""

    messages = [{"role": "user", "content": user_prompt}]
    response = invoke_llm(llm, messages)

    new_history = conversation_history + [{"user": user_input, "assistant": response.content}]

    return {
        "messages": [{"role": "assistant", "content": response.content}],
        "conversation_history": new_history
    }

# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("router", router_node)
graph_builder.add_node("vector_db", vector_db_node)
graph_builder.add_node("web_search", web_search_node)
graph_builder.add_node("generic_search", generic_search_node)
graph_builder.add_node("final_response", final_response_node)

graph_builder.add_edge(START, "router")
graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("message_type"),
    {"vector_db": "vector_db", "web_search": "web_search", "generic_search": "generic_search"}
)
graph_builder.add_edge("vector_db", "final_response")
graph_builder.add_edge("web_search", "final_response")
graph_builder.add_edge("generic_search", "final_response")
graph_builder.add_edge("final_response", END)

workflow = graph_builder.compile()

generate_graph_visualization(
    workflow,
    graph_file="outputs/agentic_workflow_diagram.png",
    hash_file="outputs/agentic_workflow_diagram.hash"
)

def main():
    print("\n" + "="*50)
    print("Agentic RAG System Ready!")
    print("="*50 + "\n")

    conversation_history = []

    while True:
        user_input = input("\nEnter your question (or 'quit' to exit): ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        print("\nProcessing...")
        response = workflow.invoke({
            "messages": [{"role": "user", "content": user_input}],
            "conversation_history": conversation_history
        })

        conversation_history = response.get("conversation_history", conversation_history)

        print("\n" + "="*50)
        print("RESPONSE:")
        print("="*50)
        last_message = response["messages"][-1]
        content = last_message.content if hasattr(last_message, 'content') else last_message["content"]
        print(content)

if __name__ == "__main__":
    main()