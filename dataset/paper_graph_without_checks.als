sig Node {
	link : set Node
}

pred DAG {
	// Directed acyclic graph
	all n: Node | n !in n.^ link
}

pred Cycle {
	// Graph with directed cycle
	some n: Node | n in n.^ link
}

pred Circular {
	// The number of nodes is equal to the number of edges and the graph has a directed cycle that visits all nodes
	#Node = #link and all n: Node | one n.link and all m, n: Node | m in n.^link
}