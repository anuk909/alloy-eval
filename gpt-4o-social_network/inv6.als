/* Problem: inv6 */

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
Influencers post every day.
*/
pred inv6 {
	all i: Influencer, d: Day | some p: i.posts | p.date = d
}

check inv6 {
    inv6 iff (all i: Influencer | Day in i.posts.date)
} for 4