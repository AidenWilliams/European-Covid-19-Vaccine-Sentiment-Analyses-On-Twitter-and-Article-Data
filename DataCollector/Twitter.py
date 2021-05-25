import pandas as pd
import tweepy


class Downloader:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.tweets = {}

    def addTweets(self, ids: list):
        tweets = self.api.statuses_lookup(ids)
        for t in tweets:
            self.tweets[t.id] = t.text

    def removeTweets(self, ids: list):
        [self.tweets.pop(key) for key in ids]


if __name__ == '__main__':
    from decouple import config

    d = Downloader(config('TWITTER_API_KEY'),
                   config('TWITTER_API_SECRET'),
                   config('TWITTER_ACCESS_TOKEN_KEY'),
                   config('TWITTER_ACCESS_TOKEN_SECRET'))

    d.addTweets([1344871397026361345, 1344871397286359041, 1344871407654731777])
    for t in d.tweets:
        print(t, ' ', d.tweets[t])

    d.removeTweets([1344871397026361345, 1344871397286359041])
    for t in d.tweets:
        print(t, ' ', d.tweets[t])
