/* Problem: graph/oriented */

sig Node {adj : set Node}

/* 
The graph is oriented, ie, contains no symmetric edges.
http://mathworld.wolfram.com/OrientedGraph.html
*/
pred oriented {
	all n1, n2: Node | n1 in n2.adj implies n2 not in n1.adj
}

check oriented {
    oriented iff (no adj & ~adj)
} for 4