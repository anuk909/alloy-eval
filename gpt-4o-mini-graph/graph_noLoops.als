/* Problem: graph/noLoops */

sig Node { adj : set Node }

/* Create an Alloy predicate 'noLoops' that checks if a graph contains no loops (nodes have no transitions to themselves).*/
pred noLoops {
	all n: Node | n !in n.adj
}

check noLoops {
    noLoops iff (no iden & adj)
} for 4