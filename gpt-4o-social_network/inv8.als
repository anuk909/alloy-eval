/* Problem: inv8 */

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
A user only sees ads from followed or suggested users.
*/
pred inv8 {
	all u: User, a: Ad | a in u.sees implies (a in u.follows.posts or a in u.suggested.posts)
}

check inv8 {
    inv8 iff (all u: User | u.sees in (u.follows.posts + u.suggested.posts))
} for 4