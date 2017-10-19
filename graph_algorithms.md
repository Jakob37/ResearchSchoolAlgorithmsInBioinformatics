# Graphs

## What are the elements of graphs?

* Points - nodes representing the elements
* Lines - edges linking the elements together in different ways

## What is a "digraph"?

Where edges have directions connected with them.

## What is meant by a "weighted graph"?

Where edges are given numerical weight.

## Explain the following graph concepts:

* Path - Finite or infinite sequences of edges connecting different nodes. A way between one node and another.
* Cycle - A closed path, where the path is looping back to an original node
* Subgraph - A subset of a full graph
* Bipartite - When decomposing a graph into two subsets where no edges directly connect nodes within a subset
* Matching - A set of edges in graph without any common nodes
* Clique - Subset of nodes in undirected graph so that if picking any two nodes within the clique, they are directly linked with an edge
* Independent set - A set of nodes where no nodes is directly connecting them

## What is a minimum spanning tree?

The smallest number or weight of edges connecting all the nodes in graph together.

## What is an Euler cycle?

A trail in graph visiting each edge exactly once returning to its starting point in the end.
Can be compared to Eulerian trail which simply visits all edges, but without needing to
cycle back to its original position.

## What is a Hamiltonian cycle?

A closed loop through a graph visiting each node exactly one time.

# Graph algorithms

## Graph traversal, what is:

* Depth-first search? - Explores as far as possible along each branch before backtracing
* Breadth-first search? - Explores all neighbors first before gradually going deeper into the graph

## What problem is the Kruskal's algorithm for?

It finds the minimum spanning tree edges.

## What is the Travelling salesman problem?

Shortest route to visit all cities? Similar to the minimum spanning tree. Can be solved with Kruskal's algorithm!
