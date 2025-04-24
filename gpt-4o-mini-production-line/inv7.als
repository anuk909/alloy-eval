/* Problem: inv7 */

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
Components built of dangerous parts are also dangerous
*/
pred inv7 {
	all p : Component | p.parts in Dangerous => p in Dangerous
}

check inv7 {
    inv7 iff (Component & parts.Dangerous in Dangerous)
} for 4