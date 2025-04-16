/* Problem: inv5 */

sig File {
  	/* A file is potentially a link to other files. */
	link : set File
}
sig Trash in File {}
sig Protected in File {}

/* 
All unprotected files are deleted..
*/
pred inv5 {
	all f: File - Protected | f in Trash
}

check inv5 {
    inv5 iff (Trash + Protected = File)
} for 4