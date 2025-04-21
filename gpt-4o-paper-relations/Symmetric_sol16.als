/* Problem: Symmetric */

sig S { r: set S }

/* 
If element x in S is related to y, then y is also related to x
*/
pred Symmetric {
	all a, b: S | a in b.r implies b in a.r
}

check Symmetric {
    Symmetric iff (all s, t: S | s->t in r implies t->s in r)
} for 4