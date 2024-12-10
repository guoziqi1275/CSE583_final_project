import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import threading
import base64
import time
import socket
from LeOpardLink import matrices

# Function to read the image and encode it as base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to load and validate the CSV file
def load_csv(file):
    try:
        df = pd.read_csv(file, header = 0, index_col= 0)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None
    
# Function to plot the graph using Jaal and open it in a new browser tab
def plot_graph(adj_matrix, port):
    G = nx.from_numpy_array(adj_matrix)
    node_df = matrices.jaal_data_prepare_node(G)
    edge_df = matrices.jaal_data_prepare_edge(G)
    edge_df['weight_vis'] = edge_df['weight'].astype(str)
    # Start a new thread to open the Jaal plot in a new browser tab
    def open_jaal_plot():
        matrices.jaal_plot(node_df = node_df, edge_df = edge_df, port = port)
    
    thread = threading.Thread(target=open_jaal_plot)
    time.sleep(0.5)
    thread.start()
    # Display the local host link in Streamlit
    st.markdown("[Open Jaal Plot](http://localhost:" + str(port) + ")")

# Function to find a free port
def find_free_port(starting_port = 8050):
    port = starting_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
            port += 1
# Background

# Function to read the image and encode it as base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Paths to images
background_image_path = "images/design/dot_transp.png"
main_page_image_path = "images/design/LOLcroped.png"

# Encode the background image
base64_image = get_base64_image(background_image_path)

# Background CSS
def get_background_css(page):
    if page == "main":
        # CSS for the main page (solid color)
        return """
        <style>
        .stApp {
            background-color: #E1C9AD; /* Light brown */
        }
        </style>
        """
    elif page == "upload":
        # CSS for the upload page (image background)
        return f"""
        <style>
        .stApp {{
            background-image: url('data:image/png;base64,{base64_image}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            color: black; /* Ensure text is readable */
        }}

        .main-content {{
            position: relative;
            z-index: 1;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            max-width: 80%;
            margin: auto;
        }}
        </style>
        """
#botton css
button_css = """
<style>
/* General button style */
div.stButton > button {
    background-color: #4CAF50; /* Green */
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}
/* Hover effect */
div.stButton > button:hover {
    background-color: #45a049; /* Darker green */
    transform: scale(1.05); /* Slightly enlarge the button */
}
/* Button focus effect */
div.stButton > button:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
"""

# Inject the CSS into Streamlit
st.markdown(button_css, unsafe_allow_html=True)

# Set default page in session state
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# Apply background CSS based on the current page
st.markdown(get_background_css(st.session_state["page"]), unsafe_allow_html=True)

# Main Page
def main_page():
    # Display the main page image
    st.image(main_page_image_path, width=600)  # Updated parameter

    # Title and input field
    st.title("Welcome to LeOpardLink!")
    name = st.text_input("What's your name:")
    if st.button("Start (click twice!)"):
        if name.strip():
            st.session_state["name"] = name
            st.session_state["page"] = "upload"  # Navigate to upload page
        else:
            st.error("Please enter a valid name.")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("© 2024 Team [LeOpardLink](https://github.com/guoziqi1275/LeOpardLink). All rights reserved.")
    st.markdown("CSE583 - Autumn 2024, University of Washington")

# Upload Page
def upload_page():
    st.title(f"Hello, {st.session_state.get('name', 'User')}!")

    #link creation area
    st.title("Create your Link here")
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
                    port = find_free_port()
                    plot_graph(adj_matrix, port)
                    

                # Generate all possible graphs
                if st.button("Generate All Possible Graphs"):
                    adj_list = matrices.create_adjlist(adj_matrix)
                    all_graphs = matrices.generate_graphs_with_transitivity(adj_list)
                    st.session_state.all_graphs = all_graphs  # Store all graphs in session state
                    st.session_state.graph_properties = matrices.graph_property(all_graphs)
                    graph_properties = matrices.graph_property(all_graphs)
                    st.write("Generated all possible graphs")
                    st.write(graph_properties)

                # Plot specific graph
                graph_id = st.text_input("Enter Graph ID to Plot")
                if st.button("Plot Specific Graph"):
                    if 'all_graphs' in st.session_state:
                        all_graphs = st.session_state.all_graphs
                        if graph_id.isdigit():
                            graph_id = int(graph_id)
                            if 0 <= graph_id < len(all_graphs):
                                specific_graph = all_graphs[graph_id]
                                specific_matrix = matrices.adjlist2matrix(specific_graph)
                                
                                port = find_free_port()
                                st.write("Using port: ", port)
                                plot_graph(specific_matrix, port)
                            
                                # Convert the specific matrix to a DataFrame for download
                                specific_df = pd.DataFrame(specific_matrix)
                                
                                # Create a CSV download button
                                csv = specific_df.to_csv(index=False, header=False)
                                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                                href = f'<a href="data:file/csv;base64,{b64}" download="specific_graph_{graph_id}.csv">Download CSV File</a>'
                                st.markdown(href, unsafe_allow_html=True)
                            else:
                                st.error("Invalid Graph ID")
                        else:
                            st.error("Please enter a valid Graph ID")
                    else:
                        st.error("Please generate all possible graphs first.")
            else:
                st.error("Invalid adjacency matrix")


    # Example usage section
    st.title("Example Usage")
    example_matrix = matrices.simulation_matrix()
    st.write("We set up an example dataset for you to explore the functionalities of LeOpardLink.")
    st.write("The example dataset is a pre-determined adjacency matrix with randomly generated uncertainties.")
    st.write("True No. individuals: 7")
    # Add a slider to adjust the uncertainty level
    uncertainty_level = st.slider("Adjust Uncertainty Level", 0.0, 1.0, 0.2, 0.1)
    example_matrix = matrices.random_uncertainties(example_matrix, uncertainty_level)
    st.session_state.example_matrix = example_matrix
    st.write(example_matrix)




    # Plot current graph
    if st.button("(Example)Plot Current Graph"):
        example_matrix = st.session_state.example_matrix
        port = find_free_port()
        plot_graph(example_matrix, port)

        # Generate all possible graphs
    if st.button("(Example)Generate All Possible Graphs"):
        st.write("(Example)Start generating")
        example_list = matrices.create_adjlist(example_matrix)
        st.write("(Example)Generated list")
        example_graphs = matrices.generate_graphs_with_transitivity(example_list)
        st.write("(Example)Generated matrix")
        st.session_state.example_graphs = example_graphs  # Store all graphs in session state
        st.write("(Example)made global")
        example_graph_properties = matrices.graph_property(example_graphs)
        st.write("(Example)Generated property")
        st.write("(Example)Generated all possible graphs")
        st.write(example_graph_properties)

            # Plot specific graph
    graph_id = st.text_input("(Example)Enter Graph ID to Plot")
    if st.button("(Example)Plot Specific Graph"):
        if 'example_graphs' in st.session_state:
            example_graphs = st.session_state.example_graphs
            if graph_id.isdigit():
                graph_id = int(graph_id)
                if 0 <= graph_id < len(example_graphs):
                    specific_graph = example_graphs[graph_id]
                    specific_matrix = matrices.adjlist2matrix(specific_graph)       
                    port = find_free_port()
                    st.write("Using port: ", port)
                    plot_graph(specific_matrix, port)
                else:
                    st.error("Invalid Graph ID")
            else:
                st.error("Please enter a valid Graph ID")
        else:
            st.error("Please generate all possible graphs first.")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("© 2024 Team [LeOpardLink](https://github.com/guoziqi1275/LeOpardLink). All rights reserved.")
    st.markdown("CSE583 - Autumn 2024, University of Washington")

# Render the appropriate page
if st.session_state["page"] == "main":
    main_page()
elif st.session_state["page"] == "upload":
    upload_page()
