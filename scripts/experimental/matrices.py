# Purpose: Implement Adjacency list with edge weights 

# import network package
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

exampleUncertain = np.array([
    [1, -1, 1, 0],
    [-1, 1, -1, 0],
    [1, -1, 1, 0],
    [0, 0, 0, 1]])


exampleTransitive = np.array([
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 1]])

exampleNotTransitive = np.array([
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 1]])

def createAdjList(adj_matrix):
    """
    Input: n x n square matrix
    Output: Adjacency List (linked list) with edge weights
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
                adj_list[row].append([column, 1])
            
            # If value is -1
            elif adj_matrix[row][column] == -1:
                adj_list[row].append([column, -1])

            # adj_matrix[row][column] == 0
            else:
                adj_list[row].append([column, 0])
    
    
    return adj_list

def sumWeights(node):
    """
    Input: List of length n (where n is number of nodes in the graph), each element is a list of length 2 (node, weight)
    Output: Int, sum of weights connected to node
    """
    sum = 0
    for connection in node:
        sum += connection[1]
    
    # this gets rid of the self connection
    sum -= 1
    return sum

def checkTransitivityWeighted(adj_list):
    """
    Input: Adjacency list with edge weights 0 or 1 (NO UNCERTAINTY!)
    Output: Bool. True if matrix is transitive, false otherwise
    """
    # get count of vertices
    vertices = len(adj_list)
    sums = [None] * vertices

    for idx, connections in enumerate(adj_list):
        sum = sumWeights(connections)
        sums[idx] = sum
        
        friends = []
        for node in connections:
            indx = node[0]
            weight = node[1]

            if weight == 1:
                friends.append(indx)
        
        for friend in friends:
            # For each friend, if the number of connections of that friend is not equal to the number of connections of our current node AND if that friend has been summed
            if sums[friend] != sum and sums[friend] != None:
                return False
            else:
                continue
    return True
