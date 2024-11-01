import numpy as np

def is_symmetric(matrix):
    """
    Check if a given square matrix is symmetric.

    Parameters:
    matrix (np.ndarray): A square numpy matrix.

    Returns:
    bool: True if the matrix is symmetric, False otherwise.
    """
    if not isinstance(matrix, np.ndarray):
        raise ValueError("Input must be a numpy array")
    
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Matrix must be square")

    return np.array_equal(matrix, matrix.T)
