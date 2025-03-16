/* Problem: graph/undirected */

sig Node { adj : set Node }

/* Create an Alloy predicate 'undirected' that checks if a graph is undirected, meaning edges are symmetric (if there's an edge from node A to node B, there must also be an edge from B to A).*/
pred undirected {
	all n1, n2 : Node | (n2 in n1.adj) implies (n1 in n2.adj)
}

check undirected {
    undirected iff (~adj = adj)
} for 4