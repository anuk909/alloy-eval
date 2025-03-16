/* Problem: graph/transitive */

sig Node { adj : set Node }

/* Create an Alloy predicate 'transitive' that checks if a directed graph is transitive, meaning if two nodes are connected through a third node, they also are connected directly.*/
pred transitive {
	all n1, n2, n3: Node | (n1.adj & n2.adj != none and n2.adj & n3.adj != none) implies n1 in n3.adj
}

check transitive {
    transitive iff (^adj = adj)
} for 4