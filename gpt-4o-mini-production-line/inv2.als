/* Problem: inv2 */

sig Workstation {
	workers : set Worker,
	succ : set Workstation
}
sig begin, end in Workstation {}
sig Worker {}
sig Human, Robot extends Worker {}
sig Product {
	parts : set Product	
}
sig Material extends Product {}
sig Component extends Product {
	workstation : set Workstation
}
sig Dangerous in Product {}

/* 
Every workstation has workers and every worker works in one workstation
*/
pred inv2 {
	all w: Workstation | w.workers = w.workers.worker \"works in\" w
}

check inv2 {
    inv2 iff (all w: Workstation | #w.workers > 0 and all wk: Worker | #(wk.~workers) = 1)
} for 4