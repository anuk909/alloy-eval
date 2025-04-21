
sig S { r: set S }

pred Connex {
    // For every pair of elements in S, either the first is related to the second or vice versa
	all s, t: S | s->t in r or t->s in r
}

pred Reflexive {
    // Every element in S is related to itself
	all s: S | s->s in r
}

pred Symmetric {
    // If element x in S is related to y, then y is also related to x
	all s, t: S | s->t in r implies t->s in r
}

pred Transitive {
    // If element x in S is related to y and y is related to z, then x is also related to z
    all s, t, u: S | s->t in r and t->u in r implies s->u in r
}

pred Antisymmetric {
    // If element x in S is related to y and y is related to x, then x and y are the same element
    all s, t: S | s->t in r and t->s in r implies s = t
}

pred Irreflexive {
    // No element in S is related to itself
    all s, t: S | s->t in r implies s != t
}

pred Functional {
    // Every element in S is related to at most one element (making r a partial function)
    all s: S | lone s.r
}

pred Function {
    // Every element in S is related to exactly one element (making r a total function)
    all s: S | one s.r
}