/* Problem: complete */

sig Node {
	adj : set Node
}

/* 
The graph is complete, ie, every node is connected to every other node.
http://mathworld.wolfram.com/CompleteDigraph.html
*/
pred complete {
	all n: Node | n.adj = Node - n
}

check complete {
    complete iff (all n: Node | Node - n = n.adj)
} for 4