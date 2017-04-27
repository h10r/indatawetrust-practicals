import datetime
import hashlib
import tweepy
#####

API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

data = api.rate_limit_status()

print "resources search"
print data["resources"]["search"]["/search/tweets"]
print( datetime.datetime.fromtimestamp( data["resources"]["search"]["/search/tweets"]["reset"] ).strftime('%Y-%m-%d %H:%M:%S') )