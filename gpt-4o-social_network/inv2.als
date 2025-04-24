/* Problem: inv2 */

sig User {
	follows : set User,
	sees : set Photo,
	posts : set Photo,
	suggested : set User
}
sig Influencer extends User {}
sig Photo {
	date : one Day
}
sig Ad extends Photo {}
sig Day {}

/* 
Users cannot follow themselves.
*/
pred inv2 {
	all u: User | u not in u.follows
}

check inv2 {
    inv2 iff (all u: User | u not in u.follows)
} for 4