/* Problem: Cycle */

sig Node {
	link : set Node
}

/* 
Graph with directed cycle
*/
pred Cycle {
	some n: Node | n in n.^link
}

check Cycle {
    Cycle iff (some n: Node | n in n.^ link)
} for 4