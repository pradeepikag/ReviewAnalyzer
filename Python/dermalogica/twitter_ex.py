import tweepy
#from textblob import TextBlob

consumer_key= 'gMLtMbtZjgjJZ8b9jT6r7Jlat'
consumer_secret= 'H1eQ8AkrSWYyMZZMowxIZ7ct494b8L7OexjsBrVQ4pQayr5pRa'
access_token='877834109975908353-rOJPqWwBI0nnIkybxaTqIzgCtjVgIKi'
access_token_secret='JMy4MuEtrtdTvgjiloeyXUAV6qXc7wy54lLTMHURen0wY'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print(api.me().name)
public_tweets = api.search('Dermalogica Daily Superfoliant')

for tweet in public_tweets:
    print(tweet.text)
    
    
    """analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
print("")"""
