import tweepy
import json


class Tweets:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.tweets = {}

    def reset(self):
        self.tweets = {}

    def addTweets(self, ids: list):
        tweets = self.api.statuses_lookup(ids)
        for t in tweets:
            self.tweets[str(t.id)] = t.text

    def removeTweets(self, ids: list):
        for id in ids:
            if str(id) in self.tweets:
                self.tweets.pop(str(id))

    def saveJSON(self, file_name):
        if '.json' not in file_name:
            file_name += '.json'
        to_save = {}
        for i, tweet in enumerate(self.tweets):
            to_save[i] = {'id': tweet, 'text': self.tweets[tweet]}
        json.dump(to_save, open(file_name, 'w+'))

    def loadJSON(self, file_name, replace=False):
        if '.json' not in file_name:
            file_name += '.json'
        if replace:
            self.tweets = json.load(open(file_name))
        else:
            tweets = json.load(open(file_name))
            self.tweets.update(tweets)

    def __repr__(self):
        """Allows the representation of Tweets as the tweets dict

        Returns
        -------
        _ngram
        """
        return self.tweets

    def __iter__(self):
        """Gives functionality to iterate over tweets
        """
        for t in self.tweets:
            yield t

    def __getitem__(self, item):
        """
        Returns
        -------
        item in tweets at index
        """
        return self.tweets[item]

    def __len__(self):
        """
        Returns
        -------
        length of tweets
        """
        return len(self.tweets)

if __name__ == '__main__':
    from decouple import config

    tweets = Tweets(config('TWITTER_API_KEY'),
                   config('TWITTER_API_SECRET'),
                   config('TWITTER_ACCESS_TOKEN_KEY'),
                   config('TWITTER_ACCESS_TOKEN_SECRET'))

    tweets.addTweets(['1344871397026361345', '1344871397286359041', '1344871407654731777'])

    tweets.removeTweets(['1344871397026361345', '1344871397286359041'])

    tweets.saveJSON('test')

    tweets.addTweets(['1344871397026361345', '1344871397286359041'])

    tweets.loadJSON('test.json')

    # print(d.tweets['1344871407654731777'])

    for t in tweets:
        print(t, ' ', tweets[t])