import json
import networkx as nx
import matplotlib.pyplot as plt

# Path to the JSON file
json_file_path = 'train.json'

# Initialize an empty list to store all the JSON objects
json_data = []

# Read the JSON file and load the objects into the list
with open(json_file_path, 'r') as file:
    for line in file:
        json_data.append(json.loads(line))

json_data = json_data[:10000]  # Limit to first 100 rows for now
# Initialize an empty directed graph
G = nx.DiGraph()

# Iterate over each entry in the JSON data
for entry in json_data:
    citing_paper = entry["paper"]
    referenced_papers = entry["reference"]
    
    # Add the citing paper node (if it doesn't exist already)
    if citing_paper not in G:
        G.add_node(citing_paper)
    
    # Add directed edges for each reference, from citing paper to referenced papers
    for reference in referenced_papers:
        G.add_edge(citing_paper, reference)

# Visualizing the graph (optional, depends on graph size)
# plt.figure(figsize=(10, 8))
# nx.draw(G, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold', alpha=0.7)
# plt.title("Citation Network")
# plt.show()

# Now you can perform SimRank calculation or other graph analysis
# Example: Calculate SimRank similarity between two papers (if they exist in the graph)
source_paper = "2805510628"
target_paper = "2160484294"

if source_paper in G and target_paper in G:
    simrank = nx.simrank_similarity(G, source=source_paper, target=target_paper, importance_factor=0.1)
    print(f"SimRank similarity between {source_paper} and {target_paper}: {simrank}")
else:
    print(f"One or both of the papers {source_paper} and {target_paper} do not exist in the graph.")
