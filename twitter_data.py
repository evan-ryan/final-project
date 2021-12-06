from twitter_api import api_key


from twitter_api import api_key
from twitter_api import api_secret
from twitter_api import access_token
from twitter_api import access_secret

import tweepy
import pandas as pd
import time
import yweather

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
# tweet_count = 1
# keyword_search = tweepy.Cursor(
#     api.search_tweets, q="New York Knicks", tweet_mode="extended", result_type="popular"
# ).items(tweet_count)
# cursor = keyword_search

class LocationNumber:
    def __init__(self, location):
        self.location = location

    def get_location(self):
        trends = api.available_trends()
        trend_locations = {}
        for i in trends:
            trend_locations[i['name']] = i['woeid']
        for k in trend_locations:
            if k == self.location:
                woe_id = trend_locations[k]
            else:
                woe_id = "Sorry Location Not Found"
        return woe_id

class UrlMaker:
    def __init__(self, id_list):
        self.id_list = id_list

    def create(self):
        url_list = []
        for item in self.id_list:
            url_list.append("https://twitter.com/twitter/statuses/" + str(item))
        return url_list



program_id = int(api.verify_credentials().id_str)
ids = []
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
                tweet_count = 2
                word = str(tag.text)
                if 'Location:' in word:
                    print('location found')
                else:
                    word_slice = word[9:]

                    keyword_search = tweepy.Cursor(
                        api.search_tweets, q=word_slice, tweet_mode="extended", result_type="popular"
                    ).items(tweet_count)
                    cursor = keyword_search

                    for i in cursor:
                        ids.append(i.id)
                    url_list = UrlMaker(ids)
                    links_list = url_list.create()
                    message = '@{} ' + ' \n'.join(links_list)
                    print(message)
                    api.update_status(message.format(tag.author.screen_name), in_reply_to_status_id=tag.id_str)
            except Exception as exc:
                print(exc)



    time.sleep(10)

# url_list = UrlMaker(ids)
# print(url_list.create())



