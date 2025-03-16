/* Problem: graph/acyclic */

sig Node { adj : set Node }

/* Create an Alloy predicate 'acyclic' that checks if a directed graph contains no cycles.*/
pred acyclic {
	all n: Node | n !in n.^adj
}

check acyclic {
    acyclic iff (no iden & ^adj)
} for 4