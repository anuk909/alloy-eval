/* Problem: inv8 */

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
Dangerous components cannot be assembled by humans
*/
pred inv8 {
	all w : Workstation | w.workers in Human implies no c : Component | c in Dangerous && c.workstation = w
}

check inv8 {
    inv8 iff (Dangerous.workstation.workers in Robot)
} for 4