# Purpose: Implement Adjacency list with edge weights 

# import packages
import numpy as np
import itertools
import copy

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

def checkSymmetric(adj_list):
    """
    Input: Adjacency list
    Output: Bool: True if symmetric False otherwise
    """
    for node, connections in enumerate(adj_list):
        for neighbor, weight in connections:
            # Check if the reciprocal connection exists using zip
            reciprocal_connections = adj_list[neighbor]
            if not any((conn == node and w == weight) for conn, w in reciprocal_connections):
                return False
    return True

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

def genCombos(adj_list):
    """
    """
    # identify all uncertain edges
    uncertain_edges = []
    
    # for each node in the list
    for idx, connections in enumerate(adj_list):
        # for each connection of each node
        for idc, friend in enumerate(connections):
            # if the connection is uncertain, track which parent node and which child node is uncertain
            if friend[1] == -1:
                uncertain_edges.append((idx, idc))
                # returns list of tuples where the 0th element is the node and the 1st element is the connection which is uncertain
    
    # Generate 2^n possible combinations
    n = len(uncertain_edges)

    # generates all 2^n possible replacement combinations
    replacement_options = list(itertools.product([0, 1], repeat=n))

    combinations = []
    for idx, replacement in enumerate(replacement_options):
        # replacement is a 4-tuple containing 0 or 1. The ith element of replacement corresponds to the ith tuple of uncertain_edges
        # temp_adjList = [list(node) for node in adj_list] # creates a copy of the original adj_list. Builds it in this manner bc of how python memory handles lists
        temp_adjList = copy.deepcopy(adj_list)
        for (idn, idc), replace in zip(uncertain_edges, replacement):
            # idn: node id
            # idc: connection id
            # [1]: weight location
            temp_adjList[idn][idc][1] = replace
        if checkTransitivityWeighted(temp_adjList) and checkSymmetric(temp_adjList):
            combinations.append(temp_adjList)
    
    return combinations

def DOESNOTWORKgenCombos(adj_list):
    """
    Generate all possible transitive combinations of an adjacency list (linked list format) by replacing -1 with 0 or 1.
    Input: adj_list: Adjacency list in linked list format, where each node's connections
                    are represented as [neighbor, weight].
                    Weights are -1 (uncertain), 0 (unconnected), or 1 (connected).
    Output:
        list: A list of adjacency lists with all possible transitive combinations.
    """
    # identify all uncertain edges
    uncertain_edges = []
    for idn, connections in enumerate(adj_list):
        for idc, friend in enumerate(connections):
            if friend[1] == -1:
                uncertain_edges.append((idn, idc))
    print(uncertain_edges)

    # number of uncertain edges
    num_uncertain = len(uncertain_edges)

    # generate all combinations of replacements (0, 1) for the uncertain edges
    replacement_options = list(itertools.product([0, 1], repeat=num_uncertain))
    print(replacement_options)

    # generate all adjacency lists with replacements
    combinations = []
    for replacement in replacement_options:
        new_adj_list = [list(node) for node in adj_list]  # Deep copy of the original list
        for (idn, idc), new_weight in zip(uncertain_edges, replacement):
            new_adj_list[idn][idc][1] = new_weight  # Update weight
        combinations.append(new_adj_list)
    
    transitiveCombos = []
    for combination in combinations:
        if checkTransitivityWeighted(combination):
            print(combination)
            transitiveCombos.append(combination)
        else:
            continue
    
    return transitiveCombos

x = createAdjList(exampleUncertain)
# print("Adjacency List: \n" + str(x))

y = genCombos(x)
print(y)
