/* Problem: undirected */

sig Node {
	adj : set Node
}

/* 
The graph is undirected, ie, edges are symmetric.
http://mathworld.wolfram.com/UndirectedGraph.html
*/
pred undirected {
	all n: Node | all m: n.adj | n in m.adj
}

check undirected {
    undirected iff (~adj = adj)
} for 4