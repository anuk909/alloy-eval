/* Problem: inv4 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
Protected files cannot be deleted.
*/
pred inv4 {
	all f: File | f in Trash => f not in Protected
}

check inv4 {
    inv4 iff (no Trash & Protected)
} for 4