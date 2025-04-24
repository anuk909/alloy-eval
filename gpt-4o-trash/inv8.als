/* Problem: inv8 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
There are no links.
*/
pred inv8 {
	all f: File | no f.link
}

check inv8 {
    inv8 iff (no File.link)
} for 4