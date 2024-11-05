import numpy as np

def is_transitive(matrix):
    """
    Check if the matrix is fully transitive (all nodes are connected with each other in a cluster). 
    
    Parameters:
    matrix (np.ndarray): A square numpy matrix.
    
    Returns:
    bool: True if the matrix is fully transitive, False otherwise.
    """
    n = matrix.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix[i, j] and matrix[j, k] and not matrix[i, k]:
                    return False
    return True
