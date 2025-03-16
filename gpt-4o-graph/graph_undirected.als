/* Problem: graph/undirected */

sig Node {adj : set Node}

/* 
The graph is undirected, ie, edges are symmetric.
http://mathworld.wolfram.com/UndirectedGraph.html
*/
pred undirected {
	all n, m: Node | n in m.adj iff m in n.adj
}

check undirected {
    undirected iff (~adj = adj)
} for 4