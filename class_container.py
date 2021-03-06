"""
Evan Ryan, Zach B, Cuba
class_container.py
Created: November 2, 2021.
Updated: December 7, 2021.
"""

from twitter_api import api_key
from twitter_api import api_key
from twitter_api import api_secret
from twitter_api import access_token
from twitter_api import access_secret
import tweepy
import time
import pyshorteners


class Auth:
    """
    Class that uses Twitter api credentials to authenticate to the api
    """

    def __init__(self, api_key, api_secret, access_token, access_secret):
        """
        Class Constructor to set class credentials as class attributes
        Input: 4 strings which coincide with Twitter api credentials
        Return: None
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret

    def init(self):
        """
        Class method for authenticating based of API credentials
        Input: Self / Class attributes: Twitter API credentials
        Return: Returns and Twitter API Object
        """
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api


api = Auth(api_key, api_secret, access_token, access_secret).init()


class LocationNumber:
    """
    Class for getting the WhereOnEarthID for a location
    """

    def __init__(self, location):
        """
        Class constructor which sets a location to a class attribute
        Input: String
        Return: None
        """
        self.location = location

    def get_location(self):
        """
        Class method for returning WhereOnEarthID for a location
        Input: Self / Class attributes: location string
        Return:
        """
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
    """
    Class for creating a list of URLs and shortening them
    """

    def __init__(self, id_list):
        """
        Class constructor which sets id_list as class attribute
        Input: id_list
            id_list: list of integers
        Output: None
        """
        self.id_list = id_list

    def create(self):
        """
        Class method to creat list of URLs
        Input: self / class attribute: list of integers
        Output: url_list
            url_list: List of URL strings
        """
        url_list = []
        for item in self.id_list:
            url_list.append("https://twitter.com/twitter/statuses/" + str(item))
        return url_list

    def shorten(self):
        """
        Class method for shortening URLS
        Input: self / class attribute: list of integers
        Output: short_list
            short_list: List of shortened URL strings
        """
        shortener = pyshorteners.Shortener()
        short_list = []
        for i in self.id_list:
            short_list.append(shortener.tinyurl.short(i))
        return short_list


class Search:
    """
    Class for Searching Twitter
    """

    def __init__(self, auth):
        """
        Class constructor for authenticating the search
        Input: API object
        Output: None
        """
        self.api = auth

    def geotag(self, woe):
        """
        Class method for searching by location
        Input: WhereOnEarthID
        Output: Formatted string to be sent to Twitter
        """
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
        """
        Class method for searching by location
        Input: keyword to search for
        Output: Formatted string to be sent to Twitter
        """
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
