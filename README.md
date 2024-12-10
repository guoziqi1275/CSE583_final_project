# LeOpardLink
[![Pylint](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/pylint.yml/badge.svg)](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/pylint.yml)
[![Python package](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/python-package.yml/badge.svg)](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/python-package.yml)
[![Python application](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/python-app.yml)
[![Python Package using Conda](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/guoziqi1275/LeOpardLink/actions/workflows/python-package-conda.yml)

**Welcome to LeOpard Link (LOL)**

!["LOL logo"](./images/design/LOL-logo-color.png)

> [!NOTE]
> Update on Dec 9th, 2024: We have a [web app](https://leopardlink.streamlit.app)! Come and try it out! 

This package is designed to assemble visual networks of detections of marked animal individuals (e.g., leopards, snow leopards, tigers, etc.) from camera-trapping datasets. We define detections as nodes in the graph, and the relationships of any pair of detections to be edges in the graph. The edges can be certain (two detections are/aren't the same individual), or uncertain (we do not know if the two detections are the same or not, e.g., detection 1 captures the left flank while detection 2 captures the right flank).

While this package was motivated for the use of wildlife camera trap images, it has many applications in other picture-relationship-based projects.

## Installation

To install the package from PyPI:

```sh
pip install LeOpardLink
```

To use streamlit UI locally:

```sh
pip install streamlit
# Inside our root directory:
streamlit run ui_code.py
```

## Dependencies
The package requires the following dependencies:

- `numpy`

- `pandas`

- `networkx`

- `jaal`>=0.1.7

## Features
- **Network Visualization:** Generate an interactive plot of the current network.

- **Graph Generation:** Generate all possible graphs from an identification matrix with uncertain edges.

- **Individual Counts:** Calculate the number of individuals, mean, standard deviation, and 95% confidence interval.

## Functions

- `check_input`: Check if the input adjacency matrix is valid. The identification matrix should only contain 3 numeric values: 1 (two detections are the same individual), 0 (two detections are not the same individual), -1 (uncertain relationship between the two detections) .

- `create_adjlist`: Create an adjacency list from an adjacency matrix. Adjcency list and matrix are two different ways to store graph information.

- `adjlist2matrix`: Convert an adjacency list to an adjacency matrix.

- `sum_weights`: Calculate the sum of weights connected to a node.

- `check_symmetric`:  Check if the graph is symmetric.

- `check_transitivity_weighted`: Check if the graph is transitive.

- `detect_conflicts`: Detect conflicts in the adjacency list.

- `strict_transitive_closure`: Compute the strict transitive closure of an adjacency matrix.

- `generate_graphs_with_transitivity`: Generate all possible graphs with transitivity from an adjacency list.

- `graph_property`: Generate a dataframe of all graphs and their properties, including the number of clusters (connected nodes).

- `get_graph_id_with_max_clusters`: Get the graph ID with the maximum number of clusters.

- `get_graph_id_with_min_clusters`: Get the graph ID with the minimum number of clusters.

- `summary`: Generate a summary of the graph properties.

- `jaal_data_prepare_node`: Prepare node data for Jaal plotting.

- `jaal_data_prepare_edge`: Prepare edge data for Jaal plotting.

- `jaal_plot`: Plot the graph using Jaal.

- `simulation_matrix`: Generate a simulation adjacency matrix.

## How does it work?

See the network below for a simulation dataset. 21 nodes represent 21 images from wildlife camera traps. Known matches are represented by edges. 
Based on this figure, there are 7 individuals.

!["simulation matrix goal"](./images/cse-583-project-simulation-matrix-drawing-1.jpg)

```python
import numpy as np
from LeOpardLink import matrices
import networkx as nx


# Example adjacency matrix
example_matrix = matrices.simulation_matrix()

# Check input
matrices.check_input(example_matrix)

# Create adjacency list
adj_list = matrices.create_adjlist(example_matrix)

# Check symmetry
matrices.check_symmetric(adj_list)

# Generate graphs with transitivity
all_graphs = matrices.generate_graphs_with_transitivity(adj_list)

# Get graph properties
graph_properties = matrices.graph_property(all_graphs)

# Plot the graph using Jaal
G = nx.from_numpy_array(matrices.adjlist2matrix(all_graphs[0]))
node_df = matrices.jaal_data_prepare_node(G)
edge_df = matrices.jaal_data_prepare_edge(G)
matrices.jaal_plot(node_df, edge_df)
```
## Try your own data!

See [this script](scripts_example/leopard.py) for a real world data usage.

## Contributing
Contributions are welcome! Please see the [issues](https://github.com/guoziqi1275/LeOpardLink/issues) page for ways you can help.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

[Courtney Allen](ckallen@uw.edu)

- Wrote documentation
- Created hand-drawn visualizations
- Example data set up
- Contributed to use cases

[Ziqi Guo](guoziqi@uw.edu)

- User interface design
- Streamlit set up
- UI technology review

[Guy Bennevat Haninovich](guybh@uw.edu)

- Coded python functions
- Wrote test cases
- Code review
- Wrote use cases

[Jiangyue Wang](jyuewang@uw.edu)

- Wrote python functions
- Wrote tests
- Wrote documentation
- Set up packaging
- Set up continuous integration via GitHub Actions
- UI implementation
