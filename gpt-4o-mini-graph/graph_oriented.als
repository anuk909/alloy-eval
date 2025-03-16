/* Problem: graph/oriented */

sig Node { adj : set Node }

/* Create an Alloy predicate 'oriented' that checks if a graph is oriented, meaning it contains no symmetric edges (if there's an edge from node A to node B, there cannot be an edge from B to A).*/
pred oriented {
	all n1, n2: Node | (n1 in n2.adj) implies (n2 not in n1.adj)
}

check oriented {
    oriented iff (no adj & ~adj)
} for 4