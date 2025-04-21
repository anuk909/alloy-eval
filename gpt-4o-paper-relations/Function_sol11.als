/* Problem: Function */

sig S { r: set S }

/* 
Every element in S is related to exactly one element (making r a total function)
*/
pred Function {
	all s: S | s.r in S and s.r != none
}

check Function {
    Function iff (all s: S | one s.r)
} for 4