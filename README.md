# LeOpardLink

**Welcome to LeOpard Link (LOL)**

This package is designed to assemble a visual network of nodes and edges that can identify potential individuals based on known relationships.

While this package was motivated for the use of wildlife camera trap images, it has many applications.

## How does it work?

See the network below. 21 nodes represent 21 images from wildlife camera traps. Known matches are represented by edges. 
Based on this figure, there are 6 individuals.

!["simulation matrix goal"](./images/cse-583-project-simulation-matrix-drawing-1.jpg)


### Two types of adjacency matrices: Certain and Uncertain Edges

An adjacency matrix from the user is necessary for this package. 
These matrices should either consis of 1s and 0s. Or an adjacency matrix with uncertain edges that contains, 1s, 0s, and 2s.

Example of Certain Adjacency Matrix:
[1,1,1,0]
[1,1,0,0]
[1,0,1,0]
[0,0,0,1] 
 *show picture of this Matrix here*


Example of Adjacency Matrix with Uncertain Edges:
[1,2,1,0]
[2,1,0,2]
[1,0,1,0]
[2,0,0,1] 
 *show picture of this Matrix here*

 Due to uncertain edges, there are several plots to show the possibilities of individual identities.