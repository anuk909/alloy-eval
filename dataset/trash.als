/**
 * First-order logic revision exercises based on a simple model of a 
 * file system trash can.
 * 
 * The model has 3 unary predicates (sets), File, Trash and
 * Protected, the latter two a sub-set of File. There is a binary 
 * predicate, link, a sub-set of File x File.
 *
 * Solve the following exercises using only Alloy's first-order 
 * logic:
 *	- terms 't' are variables
 *	- atomic formulas are either term comparisons 't1 = t2' and 
 * 't1 != t2' or n-ary predicate tests 't1 -> ... -> tn in P' and 
 * 't1 -> ... -> tn not in P'
 *	- formulas are composed by 
 *		- Boolean connectives 'not', 'and', 'or' and 'implies'
 *		- quantifications 'all' and 'some' over unary predicates
 **/

/* The set of files in the file system. */
sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
/* The set of files in the trash. */
sig Trash in File {}
/* The set of protected files. */
sig Protected in File {}

/* The trash is empty. */
pred inv1 {
	no Trash
}
check inv1 {
    inv1 iff (no Trash)
} for 4


/* All files are deleted. */
pred inv2 {
	File = Trash
}
check inv2 {
    inv2 iff (File = Trash)
} for 4


/* Some file is deleted. */
pred inv3 {
	some Trash
}
check inv3 {
    inv3 iff (some Trash)
} for 4


/* Protected files cannot be deleted. */
pred inv4 {
  	no Trash & Protected
}
check inv4 {
    inv4 iff (no Trash & Protected)
} for 4


/* All unprotected files are deleted.. */
pred inv5 {
	Trash + Protected = File
}
check inv5 {
    inv5 iff (Trash + Protected = File)
} for 4


/* A file links to at most one file. */
pred inv6 {
  	all f: File | lone f.link
}
check inv6 {
    inv6 iff (all f: File | lone f.link)
} for 4


/* There is no deleted link. */
pred inv7 {
	no File.link & Trash
}
check inv7 {
    inv7 iff (no File.link & Trash)
} for 4


/* There are no links. */
pred inv8 {
	no File.link
}
check inv8 {
    inv8 iff (no File.link)
} for 4


/* A link does not link to another link. */
pred inv9 {
  	no (File.link).link
}
check inv9 {
    inv9 iff (no (File.link).link)
} for 4


/* If a link is deleted, so is the file it links to. */
pred inv10 {
  	Trash.link in Trash
}
check inv10 {
    inv10 iff (Trash.link in Trash)
} for 4
