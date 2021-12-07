from twitter_api import api_key
from twitter_api import api_key
from twitter_api import api_secret
from twitter_api import access_token
from twitter_api import access_secret
import tweepy
import time
import pyshorteners


class Auth:
    def __init__(self, api_key, api_secret, access_token, access_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret

    def init(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api


class LocationNumber:
    def __init__(self, location):
        self.location = location

    def get_location(self):
        trends = api.available_trends()
        trend_locations = {}
        for i in trends:
            trend_locations[i["name"]] = i["woeid"]
        for k in trend_locations:
            if k == self.location:
                woe_id = trend_locations[k]

        return woe_id


class UrlMaker:
    def __init__(self, id_list):
        self.id_list = id_list

    def create(self):
        url_list = []
        for item in self.id_list:
            url_list.append("https://twitter.com/twitter/statuses/" + str(item))
        return url_list

    def shorten(self):
        shortener = pyshorteners.Shortener()
        short_list = []
        for i in self.id_list:
            short_list.append(shortener.tinyurl.short(i))
        return short_list

class Reply:
    def __init__(self):

auth = Auth(api_key, api_secret, access_token, access_secret)
api = auth.init()
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
                auth = Auth(api_key, api_secret, access_token, access_secret)
                api = auth.init()
                tweet_count = 2
                word = str(tag.text)
                if "Location:" in word:
                    print("location found")
                    word_slice = word[19:]
                    woe_id = LocationNumber(word_slice).get_location()
                    location_trend = api.get_place_trends(woe_id)
                    trend_dict = {}
                    trend_url_list = []
                    for topic in location_trend[0]["trends"][:tweet_count]:
                        trend_dict[topic["name"]] = topic["url"]
                    message = "@{} " + "\n".join(
                        " / ".join(i) for i in trend_dict.items()
                    )
                    api.update_status(
                        message.format(tag.author.screen_name),
                        in_reply_to_status_id=tag.id_str,
                    )

                else:
                    word_slice = word[9:]

                    keyword_search = tweepy.Cursor(
                        api.search_tweets,
                        q=word_slice,
                        tweet_mode="extended",
                        result_type="popular",
                    ).items(tweet_count)
                    cursor = keyword_search

                    for i in cursor:
                        ids.append(i.id)
                    url_list = UrlMaker(ids).create()
                    short_links_list = UrlMaker(url_list).shorten()
                    message = "@{} " + " \n".join(short_links_list)
                    print(message)
                    api.update_status(
                        message.format(tag.author.screen_name),
                        in_reply_to_status_id=tag.id_str,
                    )
            except Exception as exc:
                print(exc)

    time.sleep(10)
