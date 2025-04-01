/* Problem: weaklyConnected */

sig Node {
	adj : set Node
}

/* 
The graph is weakly connected, ie, it is possible to reach every node from every node ignoring edge direction.
http://mathworld.wolfram.com/WeaklyConnectedDigraph.html
*/
pred weaklyConnected {
	all n1, n2: Node | n1 in n2.adj or n2 in n1.adj
}

check weaklyConnected {
    weaklyConnected iff (Node->Node in *(adj + ~adj))
} for 4