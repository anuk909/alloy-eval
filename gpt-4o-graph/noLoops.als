/* Problem: noLoops */

sig Node {
	adj : set Node
}

/* 
The graph contains no loops, ie, nodes have no transitions to themselves.
http://mathworld.wolfram.com/GraphLoop.html
*/
pred noLoops {
	all n: Node | n not in n.adj
}

check noLoops {
    noLoops iff (no iden & adj)
} for 4