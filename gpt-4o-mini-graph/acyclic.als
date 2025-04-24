/* Problem: acyclic */

sig Node {
	adj : set Node
}

/* 
The graph is acyclic, ie, contains no directed cycles.
http://mathworld.wolfram.com/AcyclicDigraph.html
*/
pred acyclic {
	all n: Node | no (n.adj & n.*adj)
}

check acyclic {
    acyclic iff (no iden & ^adj)
} for 4