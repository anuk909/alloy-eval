/* 
Each node as a set of outgoing edges, representing a directed graph without multiple edged.
*/
sig Node {
	adj : set Node
}


/*
The graph is undirected, ie, edges are symmetric.
http://mathworld.wolfram.com/UndirectedGraph.html
*/
pred undirected {
	adj = ~adj
}

check undirected {
    undirected iff (~adj = adj)
} for 4

/*
The graph is oriented, ie, contains no symmetric edges.
http://mathworld.wolfram.com/OrientedGraph.html
*/
pred oriented {
  	no adj & ~adj
}

check oriented {
    oriented iff (no adj & ~adj)
} for 4

/*
The graph is acyclic, ie, contains no directed cycles.
http://mathworld.wolfram.com/AcyclicDigraph.html
*/
pred acyclic {
  	no iden & ^adj
}

check acyclic {
    acyclic iff (no iden & ^adj)
} for 4

/*
The graph is complete, ie, every node is connected to every other node.
http://mathworld.wolfram.com/CompleteDigraph.html
*/
pred complete {
	all n: Node | Node - n = n.adj
}

check complete {
    complete iff (all n: Node | Node - n = n.adj)
} for 4

/*
The graph contains no loops, ie, nodes have no transitions to themselves.
http://mathworld.wolfram.com/GraphLoop.html
*/
pred noLoops {
  	no iden & adj 
}

check noLoops {
    noLoops iff (no iden & adj)
} for 4

/*
The graph is weakly connected, ie, it is possible to reach every node from every node ignoring edge direction.
http://mathworld.wolfram.com/WeaklyConnectedDigraph.html
*/
pred weaklyConnected {
	Node->Node in *(adj + ~adj) 
}

check weaklyConnected {
    weaklyConnected iff (Node->Node in *(adj + ~adj))
} for 4

/*
The graph is strongly connected, ie, it is possible to reach every node from every node considering edge direction.
http://mathworld.wolfram.com/StronglyConnectedDigraph.html
*/
pred stronglyConnected {
	Node->Node in *adj
}

check stronglyConnected {
    stronglyConnected iff (Node->Node in *adj)
} for 4

/*
The graph is transitive, ie, if two nodes are connected through a third node, they also are connected directly.
http://mathworld.wolfram.com/TransitiveDigraph.html
*/
pred transitive {
    ^adj = adj
}

check transitive {
    transitive iff (^adj = adj)
} for 4