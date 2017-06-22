import tweepy
import requests
from textblob import TextBlob

company = 'deepmind'
# Twitter
consumer_key = '6OhG7BnWIzlUWDsLlrOymUh5q'
consumer_secret = 'zjG5diUDWLxBUlcFhaBmbQYH9fS03zueYqtBXDZTcfJaZMH5OD' 

access_token = '723601275183611904-p3IFufg6EjantO9SB9FrSkVAnNB3nUZ'
access_token_secret = 'XWz27ArsL0XfWlUZ6dSzJgMH1t3obyRoPD16VN1SvF1io'

# TOI
api_key = '77f402712ca04a14b0babf597b9cc2e9'
latest_data = requests.get('https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey='+api_key)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search(company)

for tweet in public_tweets:
	if not tweet.retweeted:
		print(tweet.text)
		analysis = TextBlob(tweet.text)
		print(analysis.sentiment)
		print(tweet.retweet_count)
