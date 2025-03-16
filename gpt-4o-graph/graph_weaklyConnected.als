/* Problem: graph/weaklyConnected */

sig Node { adj : set Node }

/* Create an Alloy predicate 'weaklyConnected' that checks if a directed graph is weakly connected, meaning it is possible to reach every node from every node ignoring edge direction.*/
pred weaklyConnected {
	all n: Node | n in (n.*(adj + ~adj))
}

check weaklyConnected {
    weaklyConnected iff (Node->Node in *(adj + ~adj))
} for 4