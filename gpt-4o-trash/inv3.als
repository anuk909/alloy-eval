/* Problem: inv3 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
Some file is deleted.
*/
pred inv3 {
	all f: File | f in Trash implies f !in Protected
}

check inv3 {
    inv3 iff (some Trash)
} for 4