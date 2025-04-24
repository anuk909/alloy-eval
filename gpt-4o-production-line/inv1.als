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
Workers are either human or robots
*/
pred inv1 {
	all w: Worker | w in Human + Robot
}

check inv1 {
    inv1 iff (Human + Robot = Worker)
} for 4