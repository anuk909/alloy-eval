/* Problem: Antisymmetric */

sig S { r: set S }

/* 
If element x in S is related to y and y is related to x, then x and y are the same element
*/
pred Antisymmetric {
	all x, y: S | x.r = y and y.r = x implies x = y
}

check Antisymmetric {
    Antisymmetric iff (all s, t: S | s->t in r and t->s in r implies s = t)
} for 4