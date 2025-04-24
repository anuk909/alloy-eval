/* Problem: inv4 */

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
If a user posts an ad then all its posts should be labeled as ads.
*/
pred inv4 {
	all u: User | some u.posts & Ad implies u.posts in Ad
}

check inv4 {
    inv4 iff (all u: User | (some u.posts & Ad) implies u.posts in Ad)
} for 4