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
api = tweepy.API(auth, wait_on_rate_limit=True)
# tweet_count = 1
# keyword_search = tweepy.Cursor(
#     api.search_tweets, q="New York Knicks", tweet_mode="extended", result_type="popular"
# ).items(tweet_count)
# cursor = keyword_search


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

# for i in cursor:
#     # print(dir(i))
#     tweets.append(i.full_text)
#     likes.append(i.favorite_count)
#     ids.append(i.id)

program_id = int(api.verify_credentials().id_str)

tag_id = 1
while True:
    mentions = api.mentions_timeline(since_id=tag_id)
    for tag in mentions:
        print("Tweet Found")
        print(f"{tag.author.screen_name} - {tag.text}")
        tag_id = tag.id
        if tag.in_reply_to_status_id is None and tag.author.id != program_id:
            try:
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True)
                tweet_count = 5
                word = str(tag.text)
                word_slice = word[9:]

                keyword_search = tweepy.Cursor(
                    api.search_tweets, q=word_slice, tweet_mode="extended", result_type="popular"
                ).items(tweet_count)
                cursor = keyword_search

                for i in cursor:
                    print(i.full_text)
            except Exception as exc:
                print(exc)



    time.sleep(5)

# url_list = UrlMaker(ids)
# print(url_list.create())
