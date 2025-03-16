/* Problem: graph/oriented */

sig Node { adj : set Node }

/* Create an Alloy predicate 'oriented' that checks if a graph is oriented, meaning it contains no symmetric edges (if there's an edge from node A to node B, there cannot be an edge from B to A).*/
pred oriented {
	all n, m: Node | n in m.adj implies m not in n.adj
}

check oriented {
    oriented iff (no adj & ~adj)
} for 4