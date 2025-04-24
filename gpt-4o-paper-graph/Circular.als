/* Problem: Circular */

sig Node {
	link : set Node
}

/* 
The number of nodes is equal to the number of edges and the graph has a directed cycle that visits all nodes
*/
pred Circular {
	all n: Node | #Node = #Edge and #Node = #n.*link and all n: Node | n in n.^link
}

check Circular {
    Circular iff (#Node = #link and all n: Node | one n.link and all m, n: Node | m in n.^link)
} for 4