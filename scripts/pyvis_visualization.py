from pyvis.network import Network
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import os
print("imported successfully!")

exec(open("/Users/guy/CSE583/Final/LeOpardLink/LeOpardLink/scripts/transitivity.py").read())
exec(open("/Users/guy/CSE583/Final/LeOpardLink/LeOpardLink/scripts/write-simulation-matrix-with-connections.py").read())
exec(open("/Users/guy/CSE583/Final/LeOpardLink/LeOpardLink/scripts/simuMatrix.py").read())

adj_list = createAdjList(simulationMatrix())
# print(adj_list)

net = Network(height='600px', width='800px', notebook=True, directed=False)

for node, neighbors in enumerate(adj_list):
    # Add the main node (ensure it appears even if it has no edges)
    net.add_node(node, label=str(node))
    
    # Add edges from this node to each of its neighbors
    for neighbor in neighbors:
       if node != neighbor:  # Check to prevent self-loops
            net.add_node(neighbor, label=str(neighbor))
            net.add_edge(node, neighbor)

output_file = "adjacency_list_graph.html"
net.show(output_file)

# Automatically open the HTML file in the default web browser
file_path = os.path.abspath(output_file)
webbrowser.open(f'file://{file_path}')
