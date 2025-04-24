/* Problem: Transitive */

sig S { r: set S }

/* 
If element x in S is related to y and y is related to z, then x is also related to z
*/
pred Transitive {
	all x, y, z: S | x.r & y.r != none and y.r & z.r != none implies x.r & z.r != none
}

check Transitive {
    Transitive iff (all s, t, u: S | s->t in r and t->u in r implies s->u in r)
} for 4