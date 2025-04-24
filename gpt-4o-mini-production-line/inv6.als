/* Problem: inv6 */

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
Components cannot be their own parts
*/
pred inv6 {
	all p : Component | p in p.parts => false
}

check inv6 {
    inv6 iff (all c: Component | c not in c.^parts)
} for 4