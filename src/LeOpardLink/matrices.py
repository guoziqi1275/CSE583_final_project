"""
LeOpardLink Matrices Module

This module provides functions for handling adjacency matrices 
and generating visual networks of detections of marked animal individuals. 
The functions include checking the validity of input matrices, creating adjacency lists, 
detecting conflicts, checking transitivity, and generating graphs with transitivity.
"""

# import packages
import copy
import numpy as np
import pandas as pd
import networkx as nx
from jaal import Jaal

def check_input(adj_matrix):
    """
    Input: n x n square matrix
    Output: Bool: True if input is valid, False otherwise
    """
    # Check if input is a square matrix
    if len(adj_matrix) != len(adj_matrix[0]):
        raise ValueError("Input matrix must be square!")

    # Check if input is a binary matrix
    for row in adj_matrix:
        for value in row:
            if value not in [-1, 0, 1]:
                raise ValueError("Input matrix must be numeric (-1,0,1)!")

    return True

def create_adjlist(adj_matrix):
    """
    Create an adjacency list from an adjacency matrix.
    Input: n x n square matrix
    Output: Adjacency List (linked list) with edge weights
    """
    num_verts = len(adj_matrix)

    # List of empty lists
    adj_list = [[] for _ in range(num_verts)]
    #  # Iterate through each row in the adjacency matrix
    for row in range(num_verts):
    # Iterate through each column in the current row
        for column in range(num_verts):
        # If the value in the adjacency matrix is 1
        # It means there is a path from source node to destination node
        # Add destination node to the list of neighbors from source node
            if adj_matrix[row][column] == 1:
                adj_list[row].append([column, 1])
            # If value is -1
            elif adj_matrix[row][column] == -1:
                adj_list[row].append([column, -1])

            # adj_matrix[row][column] == 0
            else:
                adj_list[row].append([column, 0])

    return adj_list

# helper function
def sum_weights(node):
    """
    Calculate the sum of weights connected to a node.
    Input: List of length n (where n is number of nodes in the graph), 
    each element is a list of length 2 (node, weight)
    Output: Int, sum of weights connected to node
    """
    sum_w = 0
    for connection in node:
        sum_w += connection[1]
    # this gets rid of the self connection
    sum_w -= 1
    return sum_w

def check_symmetric(adj_list):
    """
    Check if the graph is symmetric.
    Input: Adjacency list
    Output: Bool: True if symmetric False otherwise
    """
    for node, connections in enumerate(adj_list):
        for neighbor, weight in connections:
            # Check if the reciprocal connection exists using zip
            reciprocal_connections = adj_list[neighbor]
            if not any((conn == node and w == weight) for conn, w in reciprocal_connections):
                raise ValueError("Graph is not symmetric!")
    return True

def check_transitivity_weighted(adj_list):
    """
    Check if the graph is transitive. 
    Input: Adjacency list with edge weights 0 or 1 (NO UNCERTAINTY!)
    Output: Bool. True if matrix is transitive, false otherwise
    """
    # get count of vertices
    vertices = len(adj_list)

    # sums also plays the role of visited. If a node has not been summed it has not been visited!
    sums = [None] * vertices

    for idx, connections in enumerate(adj_list):
        # for current node, find sums
        sum_w = sum_weights(connections)

        #update sums (visited)
        sums[idx] = sum_w
        # get list of neighbors
        friends = []
        for node in connections:
            idc = node[0]
            weight = node[1]

            # if connected, track that connection
            if weight == 1:
                friends.append(idc)
        # check those neighbors
        for friend in friends:
            # For each friend, if the number of connections of that friend is not equal to
            # the number of connections of our current node AND if that friend has been summed
            if ((sums[friend] != sum_w) and (sums[friend] is not None)):
                return False
            # else:
            #     continue
    return True


def adjlist2matrix(adj_list):
    """
    Convert an adjacency list to an adjacency matrix.
    Input: adj_list. The adjacency list representing the graph.
    Output: The adjacency matrix representing the graph.
    """
    n = len(adj_list)
    adj_matrix = np.full((n, n), -1)  # Initialize with -1 for uncertain edges

    for i, neighbors in enumerate(adj_list):
        for neighbor, weight in neighbors:
            adj_matrix[i][neighbor] = weight

    return adj_matrix

def detect_conflicts(adj_list):
    """
    Detect conflicts in the adjacency list.
    Input: Adjacency list
    Output: True if no conflict, otherwise raise ValueError with conflict information
    """
    def dfs(node, visited, start_node):
        for neighbor, weight in adj_list[node]:
            if neighbor in visited:
                # Conflict detection logic
                if visited[neighbor] != weight:
                    raise ValueError(
                        f"Conflicts detected between node {node} and neighbor {neighbor}!"
                        )
                      # Conflict found
            else:
                visited[neighbor] = weight
                # If a connection is found, propagate
                if weight == 1:
                    if dfs(neighbor, visited, start_node):
                        return True
        return False

    for i in range(len(adj_list)):
        visited = {i: 1}  # Mark self-connection
        if not dfs(i, visited, i):
            return True  # No conflict detected



# helper function
def strict_transitive_closure(adj_matrix):
    """
    Compute the strict transitive closure of an adjacency matrix.
    Input: adj_matrix. The adjacency matrix representing the graph.
    Output: The strict transitive closure of the graph.
    """
    n = len(adj_matrix) # Number of vertices
    def update_transitive_edges(n, adj_matrix):
        """
        Update the adjacency matrix with transitive edges.
        Input: n. Number of vertices
               adj_matrix. The adjacency matrix representing the graph.
        Output: The adjacency matrix with transitive edges.
        """
        for i in range(n):
            for j in range(n):
                if adj_matrix[i][j] == 1:  # If there's a positive connection
                    for k in range(n):
                        if (adj_matrix[j][k] == 1 and
                            adj_matrix[i][k] == -1):  # Propagate transitivity
                            adj_matrix[i][k] = 1  # Infer positive connection
                        elif (adj_matrix[j][k] == 0 and
                            adj_matrix[i][k] == -1):  # If transitively disconnected
                            adj_matrix[i][k] = 0  # Infer negative connection
        return adj_matrix
    return update_transitive_edges(n, adj_matrix)

def generate_graphs_with_transitivity(adj_list):
    """
    Generate all possible graphs with transitivity from an adjacency list.
    Input: adj_list. The adjacency list representing the graph.
    Output: A list of all possible graphs with transitivity.
    """
    all_graphs = []
    def dfs(current_graph, uncertain_edges, index):
        """
        Perform depth-first search to generate all possible graphs.
        Input: current_graph. The current graph being processed.
               uncertain_edges. The list of uncertain edges.
               index. The index of the current uncertain edge.
        Output: None
        """
        # Base case: All uncertain edges processed
        if index == len(uncertain_edges):
            all_graphs.append(copy.deepcopy(current_graph))  # Store the graph copy
            # back change the uncertin edges (with current values 1)
            # to -1 until meeting the uncertin edge with value 0
            for backindex in range(index-1, -1, -1):
                i, j = uncertain_edges[backindex]
                if current_graph[i][j][1] == 1 | current_graph[j][i][1] == 1:
                    update_edge(current_graph, i, j, -1)
                else:
                    break
            return
        i, j = uncertain_edges[index]
        for weight in [0, 1]:  # Assign 0 or 1 to uncertain edges
            update_edge(current_graph, i, j, weight)
            if enforce_transitivity(current_graph):  # Only proceed if transitive
                dfs(current_graph, uncertain_edges, index + 1)
            # Backtrack: Reset to uncertain (-1)
            else:
                update_edge(current_graph, i, j, -1)
    def update_edge(graph, u, v, weight):
        """
        Update the edge (u, v) and its reciprocal (v, u) with the given weight.
        Input: graph. The graph to update.
               u, v. The vertices of the edge.
               weight. The weight to assign to the edge.
        Output: None
        """
        for idx, (neighbor, _) in enumerate(graph[u]):
            if neighbor == v:
                graph[u][idx][1] = weight
        for idx, (neighbor, _) in enumerate(graph[v]):
            if neighbor == u:
                graph[v][idx][1] = weight

    def enforce_transitivity(graph):
        """
        Check if the graph is transitive.
        Input: graph. The graph to check for transitivity.
        Output: True if the graph is transitive, False otherwise.
        """
        n = len(graph)
        for i in range(n):
            for j, weight_ij in graph[i]:
                if weight_ij != 1:
                    continue
                # Ensure transitive rule: if i->j and j->k, then i->k must be true
                for k, weight_jk in graph[j]:
                    if weight_jk == 1:
                        for neighbor, weight_ik in graph[i]:
                            if neighbor == k and weight_ik == 0:
                                return False  # Conflict detected
                    if weight_jk == 0:
                        for neighbor, weight_ik in graph[i]:
                            if neighbor == k and weight_ik == 1:
                                return False  # Conflict detected
        return True
    # Identify uncertain edges
    uncertain_edges = [(i, neighbor) for i in range(len(adj_list))
                       for neighbor, weight in adj_list[i] if weight == -1]
    uncertain_edges = [(i, j) for i, j in uncertain_edges if i < j]  # Remove duplicates
    dfs(copy.deepcopy(adj_list), uncertain_edges, 0)
    return all_graphs


def graph_property(all_lists):
    """
    Generate a dataframe of all graphs and their properties, 
    including number of clusters (connected components), and get an ID for each graph.

    Input: A list of adjacency lists representing the graphs.

    Returns: A DataFrame containing the graph properties.
    """
    graph_properties = []

    for idx, adj_list in enumerate(all_lists):
        # Create a graph from the adjacency list
        matrix0 = adjlist2matrix(adj_list)
        g = nx.from_numpy_array(matrix0)
        # Calculate the number of clusters (connected components)
        num_clusters = nx.number_connected_components(g)
        # Append the graph properties to the list
        graph_properties.append({
            'GraphID': idx,
            'NumClusters': num_clusters
        })
    # Create a DataFrame from the graph properties
    df = pd.DataFrame(graph_properties)
    return df

def get_graph_id_with_max_clusters(df):
    """
    Get the graph ID with the maximum number of clusters.

    Input: A DataFrame containing the graph properties.

    Returns: The graph ID with the maximum number of clusters.
    """
    return df['GraphID'][df['NumClusters'].idxmax()]

def get_graph_id_with_min_clusters(df):
    """
    Get the graph ID with the minimum number of clusters.

    Input: A DataFrame containing the graph properties.

    Returns: The graph ID with the minimum number of clusters.
    """
    return df['GraphID'][df['NumClusters'].idxmin()]

def summary(df):
    """
    Generate a summary of the graph properties.

    Input: A DataFrame containing the graph properties.

    Returns: A summary of the graph properties.
    """
    return df['NumClusters'].describe()


def jaal_data_prepare_node(g):
    """
    Prepare node data for Jaal plotting.
    Input: G. The graph to prepare node data for.
    Output: A DataFrame containing the node data.
    """
    node_g_df = pd.DataFrame(list(g.nodes(data=True)))

    node_g_df.rename(columns={0: 'id'}, inplace=True)
    node_g_df['id'] = node_g_df['id'].astype(str)
    node_g_df['title'] = 'Node' + node_g_df['id']
    node_g_df = node_g_df[['id', 'title']]
    return node_g_df

def jaal_data_prepare_edge(g):
    """
    Prepare edge data for Jaal plotting.
    Input: G. The graph to prepare edge data for.
    Output: A DataFrame containing the edge data.
    """
    edge_g_df = pd.DataFrame(list(g.edges(data=True)))
    edge_g_df.rename(columns={0: 'from', 1: 'to', 2: 'weight'}, inplace=True)
    edge_g_df['from'] = edge_g_df['from'].astype(str)
    edge_g_df['to'] = edge_g_df['to'].astype(str)
    edge_g_df['weight'] = edge_g_df['weight'].apply(lambda x: x['weight'])

    # get rid of self-loop
    edge_g_df = edge_g_df[edge_g_df['from'] != edge_g_df['to']]
    return edge_g_df

def jaal_plot(node_df, edge_df, port):
    """
    Plot the graph using Jaal.
    Input: node_df. The DataFrame containing the node data.
           edge_df. The DataFrame containing the edge data.
    Output: None. Will display the interactive graph plot.
    """
    return Jaal(edge_df, node_df).plot(port=port)

def simulation_matrix():
    """
    Generate a simulation matrix for testing purposes.
    Output: A simulation matrix for testing purposes.
    """
    matrix0 = np.array([[1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0 ,0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
    return matrix0

def random_uncertainties(matrix0, prop_uncertainty):
    """
    Generate random uncertainties in the adjacency matrix.
    Input: matrix0. The adjacency matrix.
           prop_uncertainty. The proportion of uncertain edges.
    Output: The adjacency matrix with random uncertainties.
    """
    if prop_uncertainty < 0 or prop_uncertainty > 1:
        raise ValueError("Proportion of uncertainty must be between 0 and 1!")
    no_uncertainty = int(prop_uncertainty * len(matrix0) * (len(matrix0) - 1) / 2)
    matrix = matrix0.copy()
    # Generate random uncertainties
    for i in range(no_uncertainty):
        while True:
            row = np.random.randint(0, len(matrix))
            col = np.random.randint(0, len(matrix))
            if row != col and matrix[row][col] != -1:
                matrix[row][col] = -1
                matrix[col][row] = -1
                break
    return matrix
