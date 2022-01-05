# This file collects the tweet using other method
import tweepy
import os
import json
import sys
import geocoder
import datetime

CONSUMER_KEY = "t9qZdZcMoVZdWmpjJMPbUfCNK"
CONSUMER_SECRET = "jGkcn4Jl0TQ0OehNUl3kyJceeiRa5HX5XUcd5SiLvHRtu82oo3"
ACCESS_TOKEN = "1460685525229228033-Z23GzggJxMX6wvWWZDCbs5ECxpI3n3"
ACCESS_TOKEN_SECRET = "jVcohEUtFhvmjafVcF4R8HZ8RzoR2j3pnCta9XBXvDdD5"


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)
'''
today = datetime.date.today()
yesterday= today - datetime.timedelta(days=1)
today, yesterday

tweets_list = api.search_tweets( q="#Covid-19 since:" + str(yesterday)+ " until:" + str(today),tweet_mode='extended', lang='it')

output = []
for tweet in tweets_list:
    text = tweet._json["full_text"]
    print(text)
    favourite_count = tweet.favorite_count
    retweet_count = tweet.retweet_count
    created_at = tweet.created_at
    
    line = {'text' : text, 'favourite_count' : favourite_count, 'retweet_count' : retweet_count, 'created_at' : created_at}
    output.append(line)

output

'''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

if __name__ == "__main__":
    # Available Locations
    available_loc = api.available_trends()
    # writing a JSON file that has the available trends around the world
    with open("available_locs_for_trend.json","w") as wp:
        wp.write(json.dumps(available_loc, indent=1))

    # Trends for Specific Country
    loc = "Canada"     # location as argument variable 
    g = geocoder.osm(loc) # getting object that has location's latitude and longitude

    closest_loc = api.closest_trends(g.lat, g.lng)
    trends = api.trends_place(closest_loc[0]['woeid'])
    # writing a JSON file that has the latest trends for that location
    with open("twitter_{}_trend.json".format(loc),"w") as wp:
        wp.write(json.dumps(trends, indent=1))

'''
class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        print(status.id)

# Initialize instance of the subclass
printer = IDPrinter(
  CONSUMER_KEY, CONSUMER_SECRET,
  ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

printer.filter(track=["Twitter"])

# set default threshold value 
DEFAULT_THRESHOLD = 10
# older listener with changes
class TweetListener(tweepy.Stream):
  def on_status(self, tweet):
    print(tweet.text)

listener = TweetListener(CONSUMER_KEY,CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream = tweepy.Stream(CONSUMER_KEY,CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# filter parameters
words = ['coronavirus', 'covid', 'covid19', 'covid-19', 'COVID', 'COVID19', 'COVID-19', '#covid', '#covid19', '#covid-19', '#COVID', '#COVID19', '#COVID-19']
languages = ['en']
# streaming...
stream.filter(track=words, languages=languages)
'''

