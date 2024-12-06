"""
This is the main Streamlit application file.
It contains the Streamlit UI and the functions
to load the CSV file, plot the graph, 
and generate all possible graphs.
"""

import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
from LeOpardLink import matrices
import threading
import webbrowser

# Custom CSS to set the background image
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("images/design/dot.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
st.image("images/design/LOL-logo-color.png", caption="LeOpardLink")
# Function to load and validate the CSV file
def load_csv(file):
    try:
        df = pd.read_csv(file,header=None)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

# Function to plot the graph using Jaal and open it in a new browser tab
def plot_graph(adj_matrix):
    G = nx.from_numpy_array(adj_matrix)
    node_df = matrices.jaal_data_prepare_node(G)
    edge_df = matrices.jaal_data_prepare_edge(G)
    
    # Start a new thread to open the Jaal plot in a new browser tab
    def open_jaal_plot():
        matrices.jaal_plot(node_df, edge_df)
    
    threading.Thread(target=open_jaal_plot).start()
    
    # Display the local host link in Streamlit
    st.markdown("[Open Jaal Plot](http://localhost:8050)")

# Streamlit UI
st.title("LeOpardLink Network Visualization")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file of adjacency matrix", type=["csv"])

if uploaded_file is not None:
    df = load_csv(uploaded_file)
    if df is not None:
        st.write("Adjacency Matrix:")
        st.write(df)

        # Convert DataFrame to numpy array
        adj_matrix = df.to_numpy()

        # Check input
        if matrices.check_input(adj_matrix):
            st.success("Valid adjacency matrix")

            # Plot current graph
            if st.button("Plot Current Graph"):
                plot_graph(adj_matrix)

            # Generate all possible graphs
            if st.button("Generate All Possible Graphs"):
                adj_list = matrices.create_adjlist(adj_matrix)
                all_graphs = matrices.generate_graphs_with_transitivity(adj_list)
                graph_properties = matrices.graph_property(all_graphs)
                st.write("Generated all possible graphs")
                st.write(graph_properties)

            # Plot specific graph
            graph_id = st.text_input("Enter Graph ID to Plot")
            if st.button("Plot Specific Graph"):
                if graph_id.isdigit():
                    graph_id = int(graph_id)
                    if 0 <= graph_id < len(all_graphs):
                        specific_graph = all_graphs[graph_id]
                        specific_matrix = matrices.adjlist2matrix(specific_graph)
                        plot_graph(specific_matrix)
                    else:
                        st.error("Invalid Graph ID")
                else:
                    st.error("Please enter a valid Graph ID")
        else:
            st.error("Invalid adjacency matrix")

# Example usage section
st.header("Example Usage")
example_matrix = matrices.simulation_matrix()
st.write("Example Adjacency Matrix:")
st.write(example_matrix)

if st.button("Plot Example Graph"):
    plot_graph(example_matrix)