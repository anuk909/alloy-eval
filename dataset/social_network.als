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
// Specify the following properties.
// You can check their correctness with the different commands and
// when specifying each property you can assume all the previous ones to be true.

pred inv1 {
	// Every image is posted by one user.
	all p: Photo | one posts.p
}
check inv1 {
    inv1 iff (all p: Photo | one posts.p)
} for 4

 

pred inv2 {
	// Users cannot follow themselves.
	all u: User | u not in u.follows
	// no iden & follows
}
check inv2 {
    inv2 iff (all u: User | u not in u.follows)
} for 4



pred inv3 {
	// Users can see ads posted by everyone, 
	// but only see non ads posted by followed users.
	all u: User | (u.sees - Ad) in u.follows.posts
}
check inv3 {
    inv3 iff (all u: User | (u.sees - Ad) in u.follows.posts)
} for 4



pred inv4 {
	// If a user posts an ad then all its posts should be labeled as ads. 
	all u: User | (some u.posts & Ad) implies u.posts in Ad
}
check inv4 {
    inv4 iff (all u: User | (some u.posts & Ad) implies u.posts in Ad)
} for 4



pred inv5 {
	// Influencers are followed by everyone else.
	all u: User | (Influencer - u) in u.follows
}
check inv5 {
    inv5 iff (all u: User | (Influencer - u) in u.follows)
} for 4



pred inv6 {
	// Influencers post every day.
	all i: Influencer | Day in i.posts.date
}
check inv6 {
    inv6 iff (all i: Influencer | Day in i.posts.date)
} for 4



pred inv7 {
	// Suggested are other users followed by followed users, but not yet followed.
	all u: User | u.suggested = (u.follows.follows - u.follows - u)
}
check inv7 {
    inv7 iff (all u: User | u.suggested = (u.follows.follows - u.follows - u))
} for 4



pred inv8 {
	// A user only sees ads from followed or suggested users.
	all u: User | u.sees in (u.follows.posts + u.suggested.posts)
}
check inv8 {
    inv8 iff (all u: User | u.sees in (u.follows.posts + u.suggested.posts))
} for 4
