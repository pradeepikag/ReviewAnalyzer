from __future__ import print_function
import tweepy
import json
import pymysql
from dateutil import parser
 
WORDS = ["#dermalogica","#superfoliant"]
 
CONSUMER_KEY = "gMLtMbtZjgjJZ8b9jT6r7Jlat"
CONSUMER_SECRET = "H1eQ8AkrSWYyMZZMowxIZ7ct494b8L7OexjsBrVQ4pQayr5pRa"
ACCESS_TOKEN = "877834109975908353-rOJPqWwBI0nnIkybxaTqIzgCtjVgIKi"
ACCESS_TOKEN_SECRET = "JMy4MuEtrtdTvgjiloeyXUAV6qXc7wy54lLTMHURen0wY"
 
HOST = "localhost"
USER = "root"
PASSWD = "pradeepika"
DATABASE = "twitter_rev"
 
def store_data(created_at, text, screen_name, tweet_id):
    db=pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twitter (tweet_id, scree_name, created_at, text) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (tweet_id, scree_name, created_at, text))
    db.commit()
    cursor.close()
    db.close()
    return
 
class StreamListener(tweepy.StreamListener):    
 
    def on_connect(self):
        print("You are now connected to the streaming API.")
    def on_error(self, status_code):
        print('An Error has occured: ' + repr(status_code))
        return False
    def on_data(self, data):
        try:
            dj = json.loads(data)
            text = dj['text']
            scree_name = dj['scree_name']
            tweet_id = dj['id']
            created_at = parser.parse(dj['created_at'])
            print("Tweet collected at " + str(created_at))
            store_data(created_at, text, screen_name, tweet_id)
            print(dj['text'])
        
        except Exception as e:
            print(e)
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
