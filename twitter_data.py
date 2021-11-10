from twitter_api import api_key


from twitter_api import api_key
from twitter_api import api_secret
from twitter_api import access_token
from twitter_api import access_secret

import tweepy
import pandas as pd

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
tweet_count = 1
keyword_search = tweepy.Cursor(api.search_tweets, q="New York Knicks", tweet_mode="extended").items(tweet_count)
cursor = keyword_search


tweets = []
author = []
retweets = []
likes = []
time = []

for i in cursor:
    # print(dir(i))
    tweets.append(i.full_text)
    likes.append(i.favorite_count)
    time.append(i.created_at)




df = pd.DataFrame({'tweets':tweets,'likes':likes,'time':time})
print(df)