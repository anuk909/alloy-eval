/* Problem: complete */

sig Node {
	adj : set Node
}

/* 
The graph is complete, ie, every node is connected to every other node.
http://mathworld.wolfram.com/CompleteDigraph.html
*/
pred complete {
	all n1, n2: Node | n1 != n2 implies n1.adj = n2 + n1
}

check complete {
    complete iff (all n: Node | Node - n = n.adj)
} for 4