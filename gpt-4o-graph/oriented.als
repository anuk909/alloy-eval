/* Problem: oriented */

sig Node {
	adj : set Node
}

/* 
The graph is oriented, ie, contains no symmetric edges.
http://mathworld.wolfram.com/OrientedGraph.html
*/
pred oriented {
	all n: Node | no (n.adj & n.~adj)
}

check oriented {
    oriented iff (no adj & ~adj)
} for 4