/* Problem: DAG */

sig Node {
	link : set Node
}

/* 
Directed acyclic graph
*/
pred DAG {
	all n: Node | n !in n.^link
}

check DAG {
    DAG iff (all n: Node | n !in n.^ link)
} for 4