# Background & why this matters

# User stories
1. For conservation practitioners

Dave is a conservation practitioner, he gathered leopard photos from cameras set up in the field, and he wants to identify leopards in a simple logic (i.e., decide if the two pictures are the same individual multiple ttimes). He doesn't know any coding stuff or any graph theory. He just want to do the identification task in a straightforward way and get a number of how many individuals are there.

2. For researcher (with basic coding and data structure skills)

Dave "the leopard" Becker is a researcher. Dave wants to simplify the number of images into the number of individuals in his study area. Dave is really tired of going through the images one by one (and doesn't have the funding to hire a grad student to do it for him). Dave, however, has awesome ML coding abilities and writes a ML algorithm to identify pictures of leopards (based off the spots) with some level of uncertainty. Dave has absolute faith in his ML algorithm and trusts it to create adjacency matrices that appropriately represent his images. Dave also love automation and wants to sync his ML algorithm output as an input for this project. In this case, the "user" is Dave "the leopard" Back's ML algorithm. 

3. For government officials

Dave works for the Department of Fisheries and Wildlife in the LOL State. He received a report from the researchers on leopard identification results. Dave wants to have a look at the results in an visualized and interactive way instead of reading the spreadsheet. He wants to have a interactive network graph of the existing pictures and their relationships, better with relevant information (picture ID, camera site ID) on the nodes.

4. For other people working on picture relationships but not wildlife-related.

Dave is examining historical photos of Seattle. He needs to know which photos are showing the same streets. He wants to create a visual map to connect photos in the same area.

# Data sources and structure
1. Simulation data

A graph of 21 nodes (belonging to 7 clusters) with full transitivity. We will randomly replace certain edges with uncertain edges to test the feasibility and efficiency of our functions.

2. Real leopard data

A graph of 20 nodes (belonging to 5 clusters/leopard individuals). We will use this real-world data again to test efficiency in real scenarios.

# Use cases

1. Network visualization

- Objective: Get a interactive plot of the current network

- Expected interaction: 
    - Upload csv file of matrix
    - Plot the current graph by clicking a button

2. Individual counts

- Objective: Calculate how many individuals are there, mean, sd, 95%CI

- Expected interaction
    - Upload csv file of matrix
    - Generate all possible graphs by clicking a button
    - Calculate the mean, sd, 95% CI of all possible solutions and display
    - Selectively plot some of the graphs by clicking buttons

3. Individual count - minimum case

- Objective: View the case of least individuals, get the interactive map and count the individuals

- Expected interaction
    - Upload csv file of matrix
    - Generate all possible graphs by clicking a button
    - Plot the case of least individuals, and display how many individuals are there in the plot