/* Problem: Reflexive */

sig S { r: set S }

/* 
Every element in S is related to itself
*/
pred Reflexive {
	all s: S | s.r = s.r & s
}

check Reflexive {
    Reflexive iff (all s: S | s->s in r)
} for 4