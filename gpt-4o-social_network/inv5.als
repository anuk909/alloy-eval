/* Problem: inv5 */

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
Influencers are followed by everyone else.
*/
pred inv5 {
	all u: User | Influencer in u.follows
}

check inv5 {
    inv5 iff (all u: User | (Influencer - u) in u.follows)
} for 4