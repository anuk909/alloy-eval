/* Problem: Irreflexive */

sig S { r: set S }

/* 
No element in S is related to itself
*/
pred Irreflexive {
	all s: S | s.r != s
}

check Irreflexive {
    Irreflexive iff (all s, t: S | s->t in r implies s != t)
} for 4