/* Problem: graph/complete */

sig Node { adj : set Node }

/* Create an Alloy predicate 'complete' that checks if a directed graph is complete, meaning every node has edges to all other nodes.*/
pred complete {
	all n: Node | n.adj = Node - n
}

check complete {
    complete iff (all n: Node | Node - n = n.adj)
} for 4