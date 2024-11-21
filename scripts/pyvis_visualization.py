from pyvis.network import Network
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import os
from simuMatrix import simulationMatrix
from transitivity import createAdjList


absolute_path = os.path.dirname(__file__)
relative_path = "../images/leopard.png"
full_path = os.path.join(absolute_path, relative_path)


adj_list = createAdjList(simulationMatrix())
# print(adj_list)

net = Network(height='600px', width='800px', notebook=True, directed=False)

for node, neighbors in enumerate(adj_list):
    # Add the main node (ensure it appears even if it has no edges)
    net.add_node(node, label=str(node), shape='image', image=full_path)
    
    # Add edges from this node to each of its neighbors
    for neighbor in neighbors:
       if node != neighbor:  # Check to prevent self-loops
            net.add_node(neighbor, label=str(neighbor), shape='image', image=full_path)
            net.add_edge(node, neighbor)

output_file = "adjacency_list_graph.html"
net.show(output_file)

# Automatically open the HTML file in the default web browser
file_path = os.path.abspath(output_file)
webbrowser.open(f'file://{file_path}')
