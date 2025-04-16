/* Problem: inv7 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
There is no deleted link.
*/
pred inv7 {
	all f: File | no f.link & Trash
}

check inv7 {
    inv7 iff (no File.link & Trash)
} for 4