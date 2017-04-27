import sys
import hashlib
import tweepy
from unidecode import unidecode
#####
if len(sys.argv) != 2:
    print "** ERROR: twitter_search_hashtags.py hashtag"
    sys.exit(0)

query = sys.argv[1]

API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit_notify=True)

#####

collected_nodes = []
collected_edges = []

known_hashtags = {}
known_authors = {}

#####

node_header = "nodedef> name VARCHAR, label VARCHAR, hashtag_or_author VARCHAR, full_name VARCHAR, location VARCHAR, description VARCHAR, followers_count VARCHAR"
edge_header = "edgedef> author_id VARCHAR, hashtag_id VARCHAR"

max_tweets = 1000
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

for tweet in searched_tweets:
	author_id = str(tweet.author.id)

	if author_id not in known_authors:
		new_author = ""
		new_author += author_id + ',' # name
		new_author += '"' + unidecode( tweet.author.screen_name ) + '"' + ',' # label
		new_author += '"' + "author" + '"' + ',' # hashtag_or_author
		new_author += '"' + unidecode( tweet.author.name.replace('\n',' ') ) + '"' + ',' # full_name
		new_author += '"' + unidecode( tweet.author.location.replace('\n',' ') ) + '"' + ',' # location
		new_author += '"' + unidecode( tweet.author.description.replace('\n',' ').replace('"','').replace("'",'') ) + '"' + ',' # description
		new_author += str(tweet.author.followers_count) # followers_count
		
		known_authors[ author_id ] = True

		collected_nodes.append( new_author )

	for i in range(len(tweet.entities.get('hashtags'))):
		try:
			hashtag_id = hashlib.md5( tweet.entities.get('hashtags')[i]["text"].strip() ).hexdigest()

			if hashtag_id not in known_hashtags:
				new_hashtag = ""
				new_hashtag += hashtag_id + ','
				new_hashtag += tweet.entities.get('hashtags')[i]["text"].strip() + ','
				new_hashtag += '"hashtag",' # hashtag_or_author
				new_hashtag += '"",'
				new_hashtag += '"",'
				new_hashtag += '"",'
				new_hashtag += '""'

				collected_nodes.append( new_hashtag )
			
				known_hashtags[ hashtag_id ] = True

			new_edge = ""
			new_edge += author_id + ','
			new_edge += hashtag_id

			collected_edges.append( new_edge )
		except Exception as e:
			pass

print node_header
for node in collected_nodes:
	print node
print edge_header
for edge in collected_edges:
	print edge
