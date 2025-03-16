/* Problem: inv1 */

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
when specifying each property you can assume all the previous ones to be true.
*/
pred inv1 {
	all w: Workstation | some w.workers implies some w.succ
}

check inv1 {
    inv1 iff (Human + Robot = Worker)
} for 4