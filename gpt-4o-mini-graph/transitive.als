/* Problem: transitive */

sig Node {
	adj : set Node
}

/* 
The graph is transitive, ie, if two nodes are connected through a third node, they also are connected directly.
http://mathworld.wolfram.com/TransitiveDigraph.html
*/
pred transitive {
	all n1, n2, n3: Node | (n1 in n2.adj and n2 in n3.adj) implies n1 in n3.adj
}

check transitive {
    transitive iff (^adj = adj)
} for 4