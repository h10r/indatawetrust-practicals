from collections import defaultdict

node_header = "nodedef> name VARCHAR, label VARCHAR, followers DOUBLE" # , location VARCHAR"
edge_header = "edgedef> user_to_name VARCHAR, user_from_name VARCHAR"

user_follows = defaultdict(dict)

for connection in open("../1_get_followers/petition_users_followers.tsv").readlines():
	connection_parts = connection.strip().split("\t")

	if len( connection_parts ) == 3:
		user_to, user_from, location_from = connection_parts
		user_to = user_to.replace("@", "")

		#print user_to, user_from, location_from
		user_follows[ user_to.strip() ][ user_from.strip() ] = location_from.strip()

	elif len( connection_parts ) == 2:
		user_to, user_from = connection_parts
		user_to = user_to.replace("@", "")

		user_follows[ user_to.strip() ][ user_from.strip() ] = "Unknown"

print node_header

for username, following in user_follows.items():
	print username, ",", username, ",", str( len(following) )

print edge_header

for username, following in user_follows.items():
	for follower_username, follower_location in following.items():
		print username, ",", follower_username
