#!/usr/bin/python
from twitter import *
from unidecode import unidecode

config = {}
execfile("config.py", config)

twitter = Twitter(
		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

for username in open("../all_people_in_petition.txt").readlines():
	username = unidecode( username.strip() )

	query = twitter.friends.ids(screen_name = username)

	for n in range(0, len(query["ids"]), 100):
		ids = query["ids"][n:n+100]

		subquery = twitter.users.lookup(user_id = ids)

		for user in subquery:
			print username, "\t ", unidecode( user["screen_name"] ), "\t ", unidecode( user["location"] )
