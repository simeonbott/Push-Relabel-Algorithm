# Push-Relabel-Algorithm
Python code related to the push relabel algorithm

For the original push-relabel algorithm: Goldberg A.V., Tarjan E.R.: A new approach to the maximum-flow problem. J. Assoc. Comput. Mach. 35, 921–940 (1988)
DOI: 10.1145/48014.61051

You may wish to visit other sources for a more hands-on explanation of the algorithmic process.

Usage: Push-relabel is one of many techniques for solving local flow problems, that is routing a certain amount of supply around a network starting from the source and ending at the sink. Solving a variety of flow problems, or else proving that no solution exists, on a network can tell connectivity patterns within the network itself. This type of probing is necessary due to the innate scaling complexity of networks. In particular, there is a continuous effort to find effective algorithms for working on flow problems.

The python implementation in this repository is fairly standard. The algorithm employs a deterministic lowest-label queue, and is designed to keep the runtime low, avoiding the O(n^2) normally associated with utilising nxn value tables, such as an adjacency matrix. The source and sink are listed with an entry for each node. This can be imagined as the two nodes floating outside of the network and adjacent to those nodes as indexed in the list. To use only a single source or sink, write the list with only non-zero value. The limit variable declares the label value that a node should be reach before the algorithm stops trying to push flow off of it. When debugging, it is recommended to add an additional counter to break the while loop. Limit*number_edges^2 is a good value for this.
