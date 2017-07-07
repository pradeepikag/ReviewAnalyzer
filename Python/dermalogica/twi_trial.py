from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key= 'gMLtMbtZjgjJZ8b9jT6r7Jlat'
consumer_secret= 'H1eQ8AkrSWYyMZZMowxIZ7ct494b8L7OexjsBrVQ4pQayr5pRa'
access_token='877834109975908353-rOJPqWwBI0nnIkybxaTqIzgCtjVgIKi'
access_token_secret='JMy4MuEtrtdTvgjiloeyXUAV6qXc7wy54lLTMHURen0wY'

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
stream.filter(track=['dermalogica daily superfoliant'])
