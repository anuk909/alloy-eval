/* Problem: undirected */

sig Node {
	adj : set Node
}

/* 
The graph is undirected, ie, edges are symmetric.
http://mathworld.wolfram.com/UndirectedGraph.html
*/
pred undirected {
	all n1, n2 : Node | n2 in n1.adj implies n1 in n2.adj
}

check undirected {
    undirected iff (~adj = adj)
} for 4