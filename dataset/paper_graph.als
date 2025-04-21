sig Node {
	link : set Node
}

pred DAG {
	// Directed acyclic graph
	all n: Node | n !in n.^ link
}
check DAG {
    DAG iff (all n: Node | n !in n.^ link)
} for 4


pred Cycle {
	// Graph with directed cycle
	some n: Node | n in n.^ link
}
check Cycle {
    Cycle iff (some n: Node | n in n.^ link)
} for 4


pred Circular {
	// The number of nodes is equal to the number of edges and the graph has a directed cycle that visits all nodes
	#Node = #link and all n: Node | one n.link and all m, n: Node | m in n.^link
}
check Circular {
    Circular iff (#Node = #link and all n: Node | one n.link and all m, n: Node | m in n.^link)
} for 4
