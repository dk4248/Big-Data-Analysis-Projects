import json
import networkx as nx
from collections import defaultdict
from tqdm import tqdm

# Path to the JSON file
json_file_path = 'train.json'

# Initialize an empty list to store all the JSON objects
json_data = []

# Read the JSON file and load the objects into the list
with open(json_file_path, 'r') as file:
    for line in file:
        json_data.append(json.loads(line))

# use 10% of the data
json_data = json_data[:len(json_data)//3]

# Initialize an empty directed graph
G = nx.DiGraph()

# Iterate over each entry in the JSON data
for entry in tqdm(json_data, desc="Building the graph"):
    citing_paper = entry["paper"]
    referenced_papers = entry["reference"]
    
    # Add the citing paper node (if it doesn't exist already)
    if citing_paper not in G:
        G.add_node(citing_paper)
    
    # Add directed edges for each reference, from citing paper to referenced papers
    for reference in referenced_papers:
        G.add_edge(citing_paper, reference)

# Memory-efficient SimRank function
def memory_efficient_simrank(G, query_nodes, C=0.8, num_iterations=6, top_k=10):
    """
    Memory-efficient implementation of SimRank that only computes similarities
    for specified query nodes.
    """
    # Convert query nodes to strings to ensure compatibility
    query_nodes = [str(node) for node in query_nodes]
    
    # Pre-compute in-neighbors for all nodes
    in_neighbors = {node: set(G.predecessors(node)) for node in G.nodes()}
    
    def single_pair_simrank(u, v, iteration):
        """Compute SimRank score for a single pair of nodes."""
        if u == v:
            return 1.0
        
        if iteration == 0:
            return 0.0
        
        u_in = in_neighbors[u]
        v_in = in_neighbors[v]
        
        if not u_in or not v_in:
            return 0.0
        
        score = 0.0
        for u_prev in u_in:
            for v_prev in v_in:
                score += single_pair_simrank(u_prev, v_prev, iteration - 1)
        
        return C * score / (len(u_in) * len(v_in))
    
    results = {}
    
    # For each query node
    for query_node in tqdm(query_nodes, desc="Processing query nodes"):
        if query_node not in G:
            continue
            
        similarities = []
        # Compare with all other nodes
        for other_node in tqdm(G.nodes(), desc=f"Comparing with nodes for {query_node}", leave=False):
            if str(other_node) != query_node:  # Skip self-similarity
                sim = single_pair_simrank(query_node, str(other_node), num_iterations)
                if sim > 0:  # Only store non-zero similarities
                    similarities.append((other_node, sim))
        
        # Sort by similarity score and get top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        results[query_node] = similarities[:top_k]
    
    return results

# Example usage:
query_nodes = ['1556418098', '2982615777']
C_values = [0.7, 0.8, 0.9]

results = {}
for C in tqdm(C_values, desc="Processing different C values"):
    results[C] = memory_efficient_simrank(G, query_nodes, C=C)

# Display results
for C, sim_results in results.items():
    print(f"Results for C = {C}:")
    for query_node, similarities in sim_results.items():
        print(f"  Query Node: {query_node}")
        for similar_node, score in similarities:
            print(f"    Similar Node: {similar_node}, Score: {score}")
