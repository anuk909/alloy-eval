/* Problem: inv3 */

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
Users can see ads posted by everyone,
*/
pred inv3 {
	all u: User | Ad in u.sees
}

check inv3 {
    inv3 iff (all u: User | (u.sees - Ad) in u.follows.posts)
} for 4