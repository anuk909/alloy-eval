/* Problem: inv10 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
If a link is deleted, so is the file it links to.
*/
pred inv10 {
	all f: File | f not in Trash and f not in Protected implies (no f.link or all l: f.link | l in Trash)
}

check inv10 {
    inv10 iff (Trash.link in Trash)
} for 4