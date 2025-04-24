/* Problem: inv4 */

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
Components must have parts and materials have no parts
*/
pred inv4 {
	all c: Component | some c.parts and all m: Material | no m.parts
}

check inv4 {
    inv4 iff (all c: Component | #c.parts > 0 and all m: Material | #m.parts = 0)
} for 4