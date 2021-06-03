import tweepy
import json
from string import punctuation
import re
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import six
from google.cloud import translate_v2 as translate


class Tweets:
    """The Tweets class represents a collection of tweets comprised of the id and the tweet text content.

    Various tools for processing are provided in the class to remove unwanted text features and translation.

    Version 1

    Attributes
    ----------
    api :  Tweepy API
        This is the Tweepy API object used by the class to retrieve tweets by their id.

    translate_client : Google Cloud API
        This is the Google Cloud API object used by the class to translate tweet text to english.

    tweets :  {id: text}
        A dict containing the tweets

    stopwords : {language: set(nltk.stopwords.words(language))}
        A dict of sets comprising of the nltk stopwords for each language that will be analyzed in this project

    punctuation : str
        A string of punctuations

    """
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, path_to_service_account):
        """Initialises the Tweets object using for the Twitter and Google Cloud API, aswell for the languages chosen.

        :param consumer_key: Tweepy consumer key
        :param consumer_secret: Tweepy consumer secret
        :param access_token: Tweepy access token
        :param access_token_secret: Tweepy access token secret
        :param path_to_service_account: Path to Google API service_account.json
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.translate_client = translate.Client.from_service_account_json(path_to_service_account)
        self.tweets = {}
        # dictionary of sets, very fast indeed
        self.stopwords = {
            "en": set(stopwords.words('english')),
            "fr": set(stopwords.words('french')),
            "de": set(stopwords.words('german')),
            "es": set(stopwords.words('spanish'))
        }
        self.punctuation = punctuation + '΄´’…“”–—―»«'

    def reset(self):
        """ Resets the tweets object
        """
        self.tweets = {}

    def addTweets(self, ids: list):
        """ adds tweets from the ids list to tweets

        :param ids: list of twitter tweet ids
        """
        tweets = self.api.statuses_lookup(ids)
        for t in tweets:
            self.tweets[str(t.id)] = t.text

    def removeTweets(self, ids: list):
        """ removes tweets with an id in ids from tweets

        :param ids: list of twitter tweet ids
        """
        for id in ids:
            if str(id) in self.tweets:
                self.tweets.pop(str(id))

    def saveJSON(self, file_name):
        """Saves the tweets dictionary.

        :param file_name: file name/ directory for saving
        """
        if '.json' not in file_name:
            file_name += '.json'
        to_save = {}
        for i, tweet in enumerate(self.tweets):
            to_save[i] = {'id': tweet, 'text': self.tweets[tweet]}
        json.dump(to_save, open(file_name, 'w+'))

    def loadJSON(self, file_name):
        """Loads the tweets dictionary.

        :param file_name: file name/ directory for loading
        """
        if '.json' not in file_name:
            file_name += '.json'
        jsontweets = json.load(open(file_name))
        tweets = {jsontweets[id]['id']: jsontweets[id]['text'] for id in jsontweets}
        self.tweets.update(tweets)

    def _pp(self, tweet, lang):
        """pre-processes tweet

        :param tweet: tweet
        :param lang: language of tweet
        :return: pre processed tweet
        """

        # Remove HTML special entities (e.g. &amp;)
        tweet_no_special_entities = re.sub(r'&\w*;', '', tweet)
        # Remove tickers
        tweet_no_tickers = re.sub(r'\$\w*', '', tweet_no_special_entities)
        # Remove hyperlinks
        tweet_no_hyperlinks = re.sub(r'https?://.*/\w*', '', tweet_no_tickers)
        # Remove hashtags
        tweet_no_hashtags = re.sub(r'#\w*', '', tweet_no_hyperlinks)
        # Remove Punctuation and split 's, 't, 've with a space for filter
        tweet_no_punctuation = re.sub(r'[' + punctuation.replace('@', '') + ']+', ' ', tweet_no_hashtags)
        # Remove words with 2 or fewer letters
        tweet_no_small_words = re.sub(r'\b\w{1,2}\b', '', tweet_no_punctuation)
        # Remove whitespace (including new line characters)
        tweet_no_whitespace = re.sub(r'\s\s+', ' ', tweet_no_small_words)
        # Remove single space remaining at the front of the tweet.
        tweet_no_whitespace = tweet_no_whitespace.lstrip(' ')
        # Remove characters beyond Basic Multilingual Plane (BMP) of Unicode:
        tweet_no_emojis = ''.join(c for c in tweet_no_whitespace if
                                  # Apart from emojis (plane 1), this also removes historic scripts and
                                  # mathematical alphanumerics (also plane 1),
                                  # ideographs (plane 2) and more.
                                  c <= '\uFFFF')
        # Tokenize: Change to lowercase, reduce length and remove handles
        tknzr = TweetTokenizer(preserve_case=False, reduce_len=True,
                               strip_handles=True)  # reduce_len changes, for example, waaaaaayyyy to waaayyy.
        tw_list = tknzr.tokenize(tweet_no_emojis)
        # Remove stopwords
        list_no_stopwords = [i for i in tw_list if i not in self.stopwords[lang]]
        # Final filtered tweet
        tweet_filtered = ' '.join(list_no_stopwords)
        '''
        _pp(tweet='    RT @Amila #Test\nTom\'s newly listed Co. &amp; Mary\'s unlisted     Group to supply tech for nlTK.\nh.. $TSLA $AAPL https:// t.co/x34afsfQsh', lang='en')
        '''

        return tweet_filtered

    def preProcess(self, language):
        """ preProcess all the tweets in tweets

        :param language: language of the tweets
        """
        temp_tweets = {id: self._pp(tweet=self.tweets[id], lang=language) for id in self.tweets}
        self.tweets = temp_tweets

    def _translate(self, tweet, source_language):
        """Translates text into the target language.

        :param tweet: tweet
        :param source_language: language of tweet
        :return: translated tweet from source_language to english
        """
        if isinstance(tweet, six.binary_type):
            tweet = tweet.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        return self.translate_client.translate(tweet, target_language='en', source_language=source_language)[
            "translatedText"]

    def translate(self, language):
        """ translates all the tweets in tweets to english

        :param language: language of the tweets
        """
        temp_tweets = {id: self._translate(tweet=self.tweets[id], source_language=language) for id in self.tweets}
        self.tweets = temp_tweets

    def __repr__(self):
        """Allows the representation of Tweets as the tweets dict

        Returns
        -------
        tweets
        """
        return self.tweets

    def __iter__(self):
        """Gives functionality to iterate over tweets
        """
        for tweet in self.tweets:
            yield tweet

    def __getitem__(self, item):
        """
        Returns
        -------
        item in item at index
        """
        return self.tweets[item]

    def values(self):
        """
        Returns
        -------
        item' values
        """


if __name__ == '__main__':
    from decouple import config

    tweets = Tweets(config('TWITTER_API_KEY'),
                    config('TWITTER_API_SECRET'),
                    config('TWITTER_ACCESS_TOKEN_KEY'),
                    config('TWITTER_ACCESS_TOKEN_SECRET'),
                    '../service_account.json')

    tweets.addTweets(['1344871397026361345', '1344871397286359041', '1344871407654731777'])

    tweets.removeTweets(['1344871397026361345', '1344871397286359041'])

    tweets.saveJSON('test')

    tweets.addTweets(['1344871397026361345', '1344871397286359041'])

    tweets.loadJSON('test.json')

    for t in tweets:
        print(t, ' ', tweets[t])
