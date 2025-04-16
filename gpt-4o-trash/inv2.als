/* Problem: inv2 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
All files are deleted.
*/
pred inv2 {
	all f: File | f in Trash or f in Protected
}

check inv2 {
    inv2 iff (File = Trash)
} for 4