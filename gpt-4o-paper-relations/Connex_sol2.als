/* Problem: Connex */

sig S { r: set S }

/* 
For every pair of elements in S, either the first is related to the second or vice versa
*/
pred Connex {
	all a, b: S | a != b => a.r.b or b.r.a
}

check Connex {
    Connex iff (all s, t: S | s->t in r or t->s in r)
} for 4