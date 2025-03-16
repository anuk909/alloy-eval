/* Problem: graph/oriented */

sig Node {adj : set Node}

/* 
The graph is oriented, ie, contains no symmetric edges.
http://mathworld.wolfram.com/OrientedGraph.html
*/
pred oriented {
	all n: Node, m: n.adj | m not in n.adj
}

check oriented {
    oriented iff (no adj & ~adj)
} for 4