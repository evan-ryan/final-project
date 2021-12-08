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
        woe_id = "Location not found"
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


class Search:
    def __init__(self, auth):
        self.api = auth

    def geotag(self, woe):
        tweet_count = 5
        woe_id = LocationNumber(woe).get_location()
        if isinstance(woe_id, int):
            location_trend = self.api.get_place_trends(woe_id)
            trend_dict = {}
            for topic in location_trend[0]["trends"][:tweet_count]:
                trend_dict[topic["name"]] = topic["url"]
            message = "@{} " + "\n".join(" / ".join(i) for i in trend_dict.items())
        else:
            message = "@{} " + woe_id
        return message

    def keyword(self, phrase):
        tweet_count = 10
        ids = []
        keyword_search = tweepy.Cursor(
            self.api.search_tweets,
            q=phrase,
            tweet_mode="extended",
            result_type="popular",
        ).items(tweet_count)
        cursor = keyword_search
        for i in cursor:
            ids.append(i.id)
        url_list = UrlMaker(ids).create()
        short_links_list = UrlMaker(url_list).shorten()
        key_word_message = "@{} " + " \n".join(short_links_list)
        return key_word_message
