/* Problem: inv7 */

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
Suggested are other users followed by followed users, but not yet followed.
*/
pred inv7 {
	suggested = (follows.follows - follows)
}

check inv7 {
    inv7 iff (all u: User | u.suggested = (u.follows.follows - u.follows - u))
} for 4