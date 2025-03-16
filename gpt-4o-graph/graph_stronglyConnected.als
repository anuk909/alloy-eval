/* Problem: graph/stronglyConnected */

sig Node {adj : set Node}

/* 
The graph is strongly connected, ie, it is possible to reach every node from every node considering edge direction.
http://mathworld.wolfram.com/StronglyConnectedDigraph.html
*/
pred stronglyConnected {
	all n1, n2: Node | n1 in n2.*adj
}

check stronglyConnected {
    stronglyConnected iff (Node->Node in *adj)
} for 4