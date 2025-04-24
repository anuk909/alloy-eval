/* Problem: inv3 */

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
Every component is assembled in one workstation
*/
pred inv3 {
	all c : Component | one c.workstation
}

check inv3 {
    inv3 iff (all c: Component | one c.workstation)
} for 4