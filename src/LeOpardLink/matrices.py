# Purpose: Implement Adjacency list with edge weights 

# import packages
import copy
import numpy as np
import pandas as pd
import networkx as nx
from jaal import Jaal

def checkInput(adj_matrix):
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

def createAdjList(adj_matrix):
    """
    Create an adjacency list from an adjacency matrix.
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

# helper function
def sumWeights(node):
    """
    Calculate the sum of weights connected to a node.
    Input: List of length n (where n is number of nodes in the graph), each element is a list of length 2 (node, weight)
    Output: Int, sum of weights connected to node
    """
    sumW = 0
    for connection in node:
        sumW += connection[1]
    
    # this gets rid of the self connection
    sumW -= 1
    return sumW

def checkSymmetric(adj_list):
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

def checkTransitivityWeighted(adj_list):
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
        sumW = sumWeights(connections)

        #update sums (visited)
        sums[idx] = sumW
        
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
            # For each friend, if the number of connections of that friend is not equal to the number of connections of our current node AND if that friend has been summed
            if sums[friend] != sum and sums[friend] != None:
                return False
            # else:
            #     continue
    return True


def adjListToMatrix(adj_list):
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
                    raise ValueError(f"Conflicts detected between node {node} and neighbor {neighbor}!")
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
def strictTransitiveClosure(adj_matrix):
    """
    Compute the strict transitive closure of an adjacency matrix.
    Input: adj_matrix. The adjacency matrix representing the graph.
    Output: The strict transitive closure of the graph.
    """
    n = len(adj_matrix) # Number of vertices
    
    def updateTransitiveEdges(n, adj_matrix):  
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
                        if adj_matrix[j][k] == 1 and adj_matrix[i][k] == -1:  # Propagate transitivity
                            adj_matrix[i][k] = 1  # Infer positive connection
                            
                        elif adj_matrix[j][k] == 0 and adj_matrix[i][k] == -1:  # If transitively disconnected
                            adj_matrix[i][k] = 0  # Infer negative connection
                            
        return adj_matrix
    return updateTransitiveEdges(n, adj_matrix)





def generateGraphsWithTransitivity(adj_list):
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
            # back change the uncertin edges (with current values 1) to -1 until meeting the uncertin edge with value 0
            for backindex in range(index-1, -1, -1):
                i, j = uncertain_edges[backindex]
                if current_graph[i][j][1] == 1 | current_graph[j][i][1] == 1:
                    updateEdge(current_graph, i, j, -1)
                else: 
                    break
            return
        
        i, j = uncertain_edges[index]
        
        for weight in [0, 1]:  # Assign 0 or 1 to uncertain edges
            updateEdge(current_graph, i, j, weight)
            if enforceTransitivity(current_graph):  # Only proceed if transitive
                dfs(current_graph, uncertain_edges, index + 1)
            # Backtrack: Reset to uncertain (-1)
            else:
                updateEdge(current_graph, i, j, -1)
    
    def updateEdge(graph, u, v, weight):
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

    def enforceTransitivity(graph):
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


def GraphProperty(all_lists):
    """
    Generate a dataframe of all graphs and their properties, including number of clusters (connected components), and get an ID for each graph.

    Input: A list of adjacency lists representing the graphs.

    Returns: A DataFrame containing the graph properties.
    """
    graph_properties = []

    for idx, adj_list in enumerate(all_lists):
        # Create a graph from the adjacency list
        matrix0 = adjListToMatrix(adj_list)
        G = nx.from_numpy_array(matrix0)
        
        # Calculate the number of clusters (connected components)
        num_clusters = nx.number_connected_components(G)
        
        # Append the graph properties to the list
        graph_properties.append({
            'GraphID': idx,
            'NumClusters': num_clusters
        })
    
    # Create a DataFrame from the graph properties
    df = pd.DataFrame(graph_properties)
    return df

def JaalDataPrepareNode(G):
    """
    Prepare node data for Jaal plotting.
    Input: G. The graph to prepare node data for.
    Output: A DataFrame containing the node data.
    """
    node_G = G.nodes()
    node_G_df = pd.DataFrame(list(G.nodes(data=True)))

    node_G_df.rename(columns={0: 'id'}, inplace=True)
    node_G_df['id'] = node_G_df['id'].astype(str)
    node_G_df['title'] = 'Node' + node_G_df['id']
    node_G_df = node_G_df[['id', 'title']]
    return node_G_df

def JaalDataPrepareEdge(G):
    """
    Prepare edge data for Jaal plotting.
    Input: G. The graph to prepare edge data for.
    Output: A DataFrame containing the edge data.
    """
    edge_G = G.edges()
    edge_G_df = pd.DataFrame(list(G.edges(data=True)))

    edge_G_df.rename(columns={0: 'from', 1: 'to', 2: 'weight'}, inplace=True)
    edge_G_df['from'] = edge_G_df['from'].astype(str)
    edge_G_df['to'] = edge_G_df['to'].astype(str)
    edge_G_df['weight'] = edge_G_df['weight'].apply(lambda x: x['weight'])

    # get rid of self-loop
    edge_G_df = edge_G_df[edge_G_df['from'] != edge_G_df['to']]
    return edge_G_df

def JaalPlot(node_df, edge_df):
    """
    Plot the graph using Jaal.
    Input: node_df. The DataFrame containing the node data.
           edge_df. The DataFrame containing the edge data.
    Output: None. Will display the interactive graph plot.
    """
    return Jaal(edge_df, node_df).plot()

def simulationMatrix():
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


# tmp = np.array([
#     [1, 1, 1, -1, -1, 0],
#     [1, 1, 1, -1, -1, 0],
#     [1, 1, 1, -1, -1, 0],
#     [-1, -1, -1, 1, 1, -1],
#     [-1, -1, -1, 1, 1, -1],
#     [0, 0, 0, -1, -1, 1]])    
# tmplist = createAdjList(tmp)
# all_graphs = generateGraphsWithTransitivity(tmplist)
# df = GraphProperty(all_graphs)

# graph1 = adjListToMatrix(all_graphs[0])
# graph1_node = JaalDataPrepareNode(nx.from_numpy_array(graph1))
# graph1_edge = JaalDataPrepareEdge(nx.from_numpy_array(graph1))
# JaalPlot(graph1_node, graph1_edge)


