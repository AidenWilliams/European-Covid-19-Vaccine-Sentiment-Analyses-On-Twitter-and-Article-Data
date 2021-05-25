from DataCollector.Twitter import Tweets
from decouple import config

tweets = Tweets(config('TWITTER_API_KEY'),
                config('TWITTER_API_SECRET'),
                config('TWITTER_ACCESS_TOKEN_KEY'),
                config('TWITTER_ACCESS_TOKEN_SECRET'))
