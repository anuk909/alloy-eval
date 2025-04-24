/* Problem: inv1 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
The trash is empty.
*/
pred inv1 {
	all t: Trash | no t.link
}

check inv1 {
    inv1 iff (no Trash)
} for 4