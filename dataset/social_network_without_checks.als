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
 

pred inv2 {
	// Users cannot follow themselves.
	all u: User | u not in u.follows
	// no iden & follows
}



pred inv3 {
	// Users can see ads posted by everyone, 
	// but only see non ads posted by followed users.
	all u: User | (u.sees - Ad) in u.follows.posts
}


pred inv4 {
	// If a user posts an ad then all its posts should be labeled as ads. 
	all u: User | (some u.posts & Ad) implies u.posts in Ad
}


pred inv5 {
	// Influencers are followed by everyone else.
	all u: User | (Influencer - u) in u.follows
}


pred inv6 {
	// Influencers post every day.
	all i: Influencer | Day in i.posts.date
}


pred inv7 {
	// Suggested are other users followed by followed users, but not yet followed.
	all u: User | u.suggested = (u.follows.follows - u.follows - u)
}


pred inv8 {
	// A user only sees ads from followed or suggested users.
	all u: User | u.sees in (u.follows.posts + u.suggested.posts)
}