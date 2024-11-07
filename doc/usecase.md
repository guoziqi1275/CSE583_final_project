Name: Validate User Input

Use case:
    When the user is inputting the data themselves and already has a csv file adjacency matrix

What it does:
    Takes user uploaded .csv adjacency matrix and validates that the data is encoded in a consistent manner for the rest of the compenents in the project.

Inputs:
    User uploaded .csv adjacency matrix
    3-tuple (encoding for connected edge, encoding for unconnected edge, encoding for uncertainty)

Outputs:
    Returns errors if:
        - user inputs any number of encodings not equal to 3 (connected, unconnected, uncertain)
        - user inputs encodings not represented in the matrix
        - user inputs asymmetric matrix
        - user inputs non-transitive matrix
    else:
        Returns adjacency matrix standardized so that 0 denotes unconnected edge, 1 denotes connected edge, 2 denotes uncertainty. This adjacency matrix is identical to user input.
    
Components used:
    Interface for uploading .csv file and three input boxes for connected, unconnected, uncertain
    convert_csv_to_matrix.py
    check_matrix_symmetry.py
    check_matrix_transitivity.py

Side effects:
    Data is formatted in a standardized way for the rest of the components in the project

Name: Interface