/* Problem: graph/weaklyConnected */

sig Node {adj : set Node}

/* 
The graph is weakly connected, ie, it is possible to reach every node from every node ignoring edge direction.
http://mathworld.wolfram.com/WeaklyConnectedDigraph.html
*/
pred weaklyConnected {
	let reachable = {n: Node | some path: Node -> Node | path in n.adj} | all n: Node | reachable in n.adj
}

check weaklyConnected {
    weaklyConnected iff (Node->Node in *(adj + ~adj))
} for 4