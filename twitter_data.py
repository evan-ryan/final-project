from twitter_api import api_key


from twitter_api import api_key
from twitter_api import api_secret
from twitter_api import access_token
from twitter_api import access_secret

import tweepy
import pandas as pd
import time

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
tweet_count = 1
keyword_search = tweepy.Cursor(
    api.search_tweets, q="New York Knicks", tweet_mode="extended", result_type="popular"
).items(tweet_count)
cursor = keyword_search


class UrlMaker:
    def __init__(self, id_list):
        self.id_list = id_list

    def create(self):
        url_list = []
        for item in self.id_list:
            url_list.append("https://twitter.com/twitter/statuses/" + str(item))
        return url_list


tweets = []
author = []
retweets = []
likes = []
tweet_time = []
urls = []
ids = []

for i in cursor:
    # print(dir(i))
    tweets.append(i.full_text)
    likes.append(i.favorite_count)
    ids.append(i.id)

program_id = int(api.verify_credentials().id_str)

while True:
    mentions = api.mentions_timeline()
    for tag in mentions:
        print("Mention Tweet Found")
        print(f"{tag.author.screen_name} - {tag.text}")

    time.sleep(5)

# url_list = UrlMaker(ids)
# print(url_list.create())
