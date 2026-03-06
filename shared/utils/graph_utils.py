"""
Utility functions for LangGraph visualization and management.
Production-ready, reusable across multiple graph implementations.
"""

import os
import hashlib


def should_regenerate_graph(workflow, graph_file, hash_file):
    """
    Determine if graph visualization needs regeneration.
    
    Args:
        workflow: Compiled LangGraph workflow
        graph_file: Path to output PNG file
        hash_file: Path to hash storage file
    
    Returns:
        tuple: (bool: needs_regeneration, str: reason)
    """
    # If graph file doesn't exist, we need to generate
    if not os.path.exists(graph_file):
        return True, "Graph file doesn't exist"
    
    # Get current graph structure hash
    graph_structure = workflow.get_graph().draw_mermaid()
    current_hash = hashlib.md5(graph_structure.encode()).hexdigest()
    
    # If hash file doesn't exist, regenerate
    if not os.path.exists(hash_file):
        return True, "Hash file doesn't exist"
    
    # Compare with stored hash
    try:
        with open(hash_file, 'r') as f:
            stored_hash = f.read().strip()
        
        if stored_hash != current_hash:
            return True, "Graph structure changed"
        
        return False, "Graph unchanged"
    except Exception as e:
        return True, f"Error reading hash: {e}"


def generate_graph_visualization(workflow, graph_file="outputs/workflow_diagram.png", hash_file="outputs/workflow_diagram.hash"):
    """
    Generate graph visualization only when necessary.
    Production-ready with proper error handling and logging.
    
    Args:
        workflow: Compiled LangGraph workflow
        graph_file: Path to output PNG file (default: outputs/workflow_diagram.png)
        hash_file: Path to hash storage file (default: outputs/workflow_diagram.hash)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Ensure outputs directory exists
    os.makedirs(os.path.dirname(graph_file), exist_ok=True)
    
    needs_regen, reason = should_regenerate_graph(workflow, graph_file, hash_file)
    
    if needs_regen:
        print(f"Regenerating graph: {reason}")
        try:
            # Generate the PNG
            workflow.get_graph().draw_mermaid_png(output_file_path=graph_file)
            
            # Save the hash for future comparisons
            graph_structure = workflow.get_graph().draw_mermaid()
            current_hash = hashlib.md5(graph_structure.encode()).hexdigest()
            with open(hash_file, 'w') as f:
                f.write(current_hash)
            
            print(f"✓ Graph successfully saved as {graph_file}")
            return True
            
        except Exception as e:
            print(f"Error generating graph: {e}")
            print("Tip: Ensure pygraphviz is installed: pip install pygraphviz")
            return False
    else:
        print(f"✓ Using existing graph: {reason}")
        return True