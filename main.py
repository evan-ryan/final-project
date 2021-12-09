"""
Evan Ryan, Zach B, Cuba
main.py
Created: November 2, 2021.
Updated: December 7, 2021.
"""
from twitter_api import api_key
from twitter_api import api_key
from twitter_api import api_secret
from twitter_api import access_token
from twitter_api import access_secret
from class_container import Auth
from class_container import LocationNumber
from class_container import UrlMaker
from class_container import Search
import tweepy
import time
import pyshorteners


def main():
    """
    Function for running main program loop
    """
    api = Auth(api_key, api_secret, access_token, access_secret).init()
    # setting our id for a program to compare
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
                    api = Auth(api_key, api_secret, access_token, access_secret).init()

                    word = str(tag.text)
                    # if statement for location search
                    if "Location:" in word:
                        print("Searching for Trends in Location")
                        woe_tweet = word[19:]
                        message = Search(api).geotag(woe_tweet)
                        api.update_status(
                            message.format(tag.author.screen_name),
                            in_reply_to_status_id=tag.id_str,
                        )
                    # else statement for keyword search
                    else:
                        word_slice = word[9:]
                        message = Search(api).keyword(word_slice)
                        api.update_status(
                            message.format(tag.author.screen_name),
                            in_reply_to_status_id=tag.id_str,
                        )
                except Exception as exc:
                    print(exc)
        # sleep to combat API rate limits
        time.sleep(10)


if __name__ == "__main__":
    main()
