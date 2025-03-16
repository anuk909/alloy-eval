/* Problem: graph/acyclic */

sig Node { adj : set Node }

/* Create an Alloy predicate 'acyclic' that checks if a directed graph contains no cycles.*/
pred acyclic {
	no Node | (this in Node.adj) // Ensure no node points to itself
    all n: Node | no n.adj & (n in Node) // No node has a path back to itself
    all n: Node | no n.adj & (n in Node.adj) // No node is reachable from itself through its adjacency
}

check acyclic {
    acyclic iff (no iden & ^adj)
} for 4