# List of components

- Component 1: User interface (several buttons on a screen) to let user decide what they want to do. Input: user clicks. Output: to corresponding pages.
	- Upload matrix
	- Plot current graph
	- Generate all possible graphs
	- Plot out specific graph among all possibilities
	- Export all possible graphs (in the format of adjacency matrix)

- Component 2: Upload CSV of adjacency matrix and check format (or use our simulation data). Input from user upload or our simulation data, output is a standardized adjacency matrix.
	- Interactive 1: "Upload" button, "Simulation data" button
	- Interactive 2: pop up new window to specify directory of the CSV file
	- Functions to check CSV format (authentication)
		- Function 1: Is it in the format that we want (matrix with values of 0,1,2)? 
		- Function 2: Are there any conflicts in the matrix?
		- Function 5: check transitivity

- Component 3: Plot current graph (treat 2 as 0 if there's still 2s in the matrix) Input: matrix from component 2. Output: an interactive network plot.
	- Function 3: call Jaal

- Component 4: Generate all possible graphs. Input: matrix from component 2. Output: a list of all possible graph adjacency lists; a dataframe for graph features.
	- Function 4: convert adjacency matrix to adjacency list (Done)
	- Function 5: check transitivity (Done)
	- Function 6: Achieve full transitivity (convert 2 to 0/1 based on related nodes) to reduce uncertainty
	- Function 7: List all possible graphs without any uncertain edges (store them in a list of adjacency list)
	- Function 8: generate a dataframe to store the features of all graphs (no. inds, graph ID)


- Component 5: Plot out specific graph among all possibilities. Input: user input (graph ID), list and dataframe from component 4. Output: an interactive plot of that specific graph.
	- Interactive 3: User input window: Give message of how many graphs are there, give 2 buttons for least and  most no. inds, then a text box to type in graph ID
	- Function 9: covert adjacency list back to matrix
	- Function 10: get user input: "least no. inds", "most no. inds", or graph ID, and pass the corresponding graph ID to Function 3
	- Function 3: call Jaal

[comment]: # Maybe not doing this component for now...
[comment]: # - Component 6: Export all possible graphs (in the format of adjacency matrix). [comment]: # Input: file directory, list from component 4. Output: lots of csv files.
[comment]: # 	- Interactive 4: a pop-up window to let user decide where to store all the matrices
[comment]: # 	- Function 9: covert adjacency list back to matrix
[comment]: # 	- Function 11: write out all matrices one by one to csv

# Interactions to complete use cases
1. Network visualization

- Component 1
- Component 2
- Component 3

2. Individual counts

- Component 1
- Component 2
- Component 4
- Component 5

3. Individual count - minimum case

- Component 1
- Component 2
- Component 4
- Component 5

# Plan

 1. All functions needed (try to improve complexity, now we have O(2^(n^2))...) - Week 10
 2. Connect our package to streamlit - Week 10
 3. Make our package downloadable/installable via github, pip, or conda - Week 11
 4. Fully connect our package to streamlit webapp - Week 11
 5. Full documentation of function usage, tutorial, citations, environments - Week 12 before ddl 






