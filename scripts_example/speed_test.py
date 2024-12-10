"""
This script is used to test the speed of the LeOpardLink package with parallel computing.
"""
import numpy as np
import pandas as pd
import networkx as nx
import time
import random
import multiprocessing
from joblib import Parallel, delayed

from LeOpardLink import matrices

def generate_matrix(n, c):
    """
    Generate a random matrix that is transitive and symmetric.
    
    Parameters:
    -----------
    n : int
        Number of nodes
    c : int
        Number of clusters
    
    Returns:
    --------
    np.array
        A random matrix
    """
    # Ensure we don't create more clusters than nodes
    c = min(c, n)
    
    # Generate cluster sizes more efficiently
    cluster_sizes = [max(1, n // c + (1 if i < n % c else 0)) for i in range(c)]
    
    # Ensure total nodes match n
    assert sum(cluster_sizes) == n, "Cluster sizes do not match total nodes"
    
    # Generate a random partition graph with no inter-cluster connections
    G = nx.random_partition_graph(cluster_sizes, 1, 0)
    
    # Convert the graph to a numpy adjacency matrix
    matrix = nx.to_numpy_array(G)
    
    # Make diagonal 1 and convert to integers
    np.fill_diagonal(matrix, 1)
    matrix = matrix.astype(int)
    
    return matrix

def process_single_experiment(n, c, p, seed):
    """
    Process a single experiment with given parameters.
    
    Parameters:
    -----------
    n : int
        Number of nodes
    c : int
        Number of clusters
    p : float
        Proportion of uncertainty
    seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    dict
        Results of the experiment
    """
    # Set random seeds for reproducibility
    random.seed(seed)
    np.random.seed(seed)
    
    try:
        # Generate random matrix
        matrix = generate_matrix(n, c)
        
        # Add uncertainties
        matrix0 = matrices.random_uncertainties(matrix, p)
        
        # Measure time for graph generation
        start_time = time.time()
        all_graphs = matrices.generate_graphs_with_transitivity(matrices.create_adjlist(matrix0))
        end_time = time.time()
        
        # Get estimated clusters
        estimated_clusters = matrices.graph_property(all_graphs)['NumClusters']
        
        return {
            'n': n,
            'c': c,
            'p': p,
            'time': end_time - start_time,
            'estimated_clusters': estimated_clusters,
            'seed': seed
        }
    
    except Exception as e:
        print(f"Error processing n={n}, c={c}, p={p}, seed={seed}: {e}")
        return None

def run_speed_test(n_jobs=None):
    """
    Conduct speed tests for LeOpardLink package with various parameters.
    
    Parameters:
    -----------
    n_jobs : int, optional
        Number of parallel jobs. If None, uses all available CPU cores.
    
    Returns:
    --------
    pd.DataFrame
        Results of speed tests
    """
    # Parameters for testing
    n_values = [10, 25, 50, 100, 200, 500, 1000]
    c_values = [2, 5, 10, 20, 50, 100]
    p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    # Prepare all experiment configurations
    experiments = [
        (n, c, p, seed)
        for n in n_values
        for c in c_values if c <= n
        for p in p_values
        for seed in range(99)
    ]
    
    # Determine number of jobs
    if n_jobs is None:
        n_jobs = multiprocessing.cpu_count()
    
    # Run experiments in parallel
    results_list = Parallel(n_jobs=n_jobs)(
        delayed(process_single_experiment)(n, c, p, seed) 
        for n, c, p, seed in experiments
    )
    
    # Filter out None results (failed experiments)
    results_list = [result for result in results_list if result is not None]
    
    # Convert results to DataFrame
    results = pd.DataFrame(results_list)
    
    # Save results
    results.to_csv('data/speed_test_results.csv', index=False)
    
    return results

# Run the speed test if the script is executed directly
if __name__ == "__main__":
    # Run with all available CPU cores
    results = run_speed_test()
    
    # Alternatively, specify number of jobs
    # results = run_speed_test(n_jobs=4)
    
    print(results)