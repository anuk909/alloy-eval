/* Problem: graph/stronglyConnected */

sig Node { adj : set Node }

/* Create an Alloy predicate 'stronglyConnected' that checks if a directed graph is strongly connected, meaning it is possible to reach every node from every node considering edge direction.*/
pred stronglyConnected {
	all n, m: Node | n in m.*adj
}

check stronglyConnected {
    stronglyConnected iff (Node->Node in *adj)
} for 4