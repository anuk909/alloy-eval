/* Problem: graph/weaklyConnected */

sig Node { adj : set Node }

/* Create an Alloy predicate 'weaklyConnected' that checks if a directed graph is weakly connected, meaning it is possible to reach every node from every node ignoring edge direction.*/
pred weaklyConnected {
	all n1, n2: Node | n1 in n2.*adj or n2 in n1.*adj
}

check weaklyConnected {
    weaklyConnected iff (Node->Node in *(adj + ~adj))
} for 4