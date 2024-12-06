import numpy as np
import pandas as pd
from LeOpardLink import matrices
import networkx as nx


matrix_leopard = pd.read_csv("data/real_leopard_matrix.csv")
matrix_leopard.set_index('colnames(tmp)', inplace=True)
matrix_leopard_array = matrix_leopard.to_numpy()

# Check input
matrices.checkInput(matrix_leopard_array) # Get Value Error cause uncertain edges are "2"

# Modify uncertain edges to -1
example_matrix = np.where(matrix_leopard_array == 2, -1, matrix_leopard_array)
# Check input
matrices.checkInput(example_matrix)

# Plot out current graph
G0 = nx.from_numpy_array(example_matrix)
node_df = matrices.JaalDataPrepareNode(G0)
edge_df = matrices.JaalDataPrepareEdge(G0)
# add another column that is identical to weight but named differently and make it string, so we can visualize edges in different colors
edge_df['weight_vis'] = edge_df['weight'].astype(str)
# add another column to nodes that is the detection name
node_df['detection_id'] = matrix_leopard.columns
node_df['site'] = node_df['detection_id'].apply(lambda x: x.split('-A')[0])
# Use query "weight>0" to filter out the edges with weight > 0
matrices.JaalPlot(node_df, edge_df)


# Create adjacency list
adj_list = matrices.createAdjList(example_matrix)

# Check symmetry
matrices.checkSymmetric(adj_list)

# Generate graphs with transitivity
all_graphs = matrices.generateGraphsWithTransitivity(adj_list)

# Get graph properties
graph_properties = matrices.GraphProperty(all_graphs)
matrices.Summary(graph_properties)

# get the graph id with the minimum individuals
minID = matrices.getGraphIDwithMinClusters(graph_properties)
# Plot the graph using Jaal
G = nx.from_numpy_array(matrices.adjListToMatrix(all_graphs[minID]))
node_df = matrices.JaalDataPrepareNode(G)
edge_df = matrices.JaalDataPrepareEdge(G)

# CUSTOMIZE THE PLOT
# add another column that is identical to weight but named differently and make it string, so we can visualize edges in different colors
edge_df['weight_vis'] = edge_df['weight'].astype(str)
# add another column to nodes that is the detection name
node_df['detection_id'] = matrix_leopard.columns
node_df['site'] = node_df['detection_id'].apply(lambda x: x.split('-A')[0])
# Use query "weight>0" to filter out the edges with weight > 0
matrices.JaalPlot(node_df, edge_df)