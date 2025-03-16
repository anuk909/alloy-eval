sig Workstation {
	workers : set Worker,
	succ : set Workstation
}
one sig begin, end in Workstation {}

sig Worker {}
sig Human, Robot extends Worker {}

abstract sig Product {
	parts : set Product	
}

sig Material extends Product {}

sig Component extends Product {
	workstation : set Workstation
}

sig Dangerous in Product {}
// Specify the following properties.
// You can check their correctness with the different commands and
// when specifying each property you can assume all the previous ones to be true.

pred inv1 {
	// Workers are either human or robots
	Human + Robot = Worker
}


pred inv2 {
	// Every workstation has workers and every worker works in one workstation
	all w: Workstation | #w.workers > 0 and all wk: Worker | #(wk.~workers) = 1
}


pred inv3 {
	// Every component is assembled in one workstation
	all c: Component | one c.workstation
}


pred inv4 {
	// Components must have parts and materials have no parts
	all c: Component | #c.parts > 0 and all m: Material | #m.parts = 0
}


pred inv5 {
	// Humans and robots cannot work together
	all w: Workstation | w.workers in Human or w.workers in Robot
}

pred inv6 {
	// Components cannot be their own parts
	all c: Component | c not in c.^parts
}

pred inv7 {
	// Components built of dangerous parts are also dangerous
	Component & parts.Dangerous in Dangerous
}

pred inv8 {
	// Dangerous components cannot be assembled by humans
	Dangerous.workstation.workers in Robot
}

pred inv9 {
	// The workstations form a single line between begin and end
	no succ.begin and no end.succ and all w: Workstation - end | one w.succ and all w: Workstation - begin | one succ.w and Workstation = begin.*succ
}

pred inv10 {
	// The parts of a component must be assembled before it in the production line
	all c: Component | all p: c.parts & Component | some (c.workstation & p.workstation.^succ)
}