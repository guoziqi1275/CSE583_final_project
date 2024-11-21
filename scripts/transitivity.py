# Purpose: Functions for data verification
# Created by: Guy Bennevat Haninovich, Nov 4th, 2024
# Last modified: Nov 4th, 2024

# import network package
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def createAdjList(adj_matrix):
    """
    Input: n x n square matrix
    Output: Adjacency List (linked list)
    """
    numVerts = len(adj_matrix)

    # List of empty lists 
    adj_list = [[] for _ in range(numVerts)]
    #  # Iterate through each row in the adjacency matrix
    
    for row in range(numVerts):
    # Iterate through each column in the current row
        for column in range(numVerts):
        # If the value in the adjacency matrix is 1
        # It means there is a path from source node to destination node
        # Add destination node to the list of neighbors from source node
            if adj_matrix[row][column] == 1:
                adj_list[row].append(column)
    
    return adj_list

def checkTransitivity(adj_matrix):
    """
    Input: n x n square matrix already checked for symmetry.
    Output: Bool. True if matrix is transitive, false otherwise
    """
    adj_list = createAdjList(adj_matrix)

    # get count of vertices 
    vertices = len(adj_list)

    # nothing has been visited
    visited = [-1] * vertices

    for i in range (0, vertices):
        # if this node is not visited
        if visited[i] == -1:
            nodes = adj_list[i]
            sub_edges = len(nodes)

            for node in nodes:
                if nodes != adj_list[node]:
                    return False
                else:
                    visited[node] = 1

            # mark node as visited
            visited[i] = 1
        else:
            # node has already been checked no need to check again
            continue
    
    return True

