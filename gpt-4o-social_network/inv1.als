/* Problem: inv1 */

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
Every image is posted by one user.
*/
pred inv1 {
	all p: Photo | one u: User | p in u.posts
}

check inv1 {
    inv1 iff (all p: Photo | one posts.p)
} for 4