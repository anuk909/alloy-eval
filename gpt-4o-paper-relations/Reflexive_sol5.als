/* Problem: Reflexive */

sig S { r: set S }

/* 
Every element in S is related to itself
*/
pred Reflexive {
	all s: S | s in s.r and s.r = s.r
}

check Reflexive {
    Reflexive iff (all s: S | s->s in r)
} for 4