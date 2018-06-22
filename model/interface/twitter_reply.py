import os
from dotenv import load_dotenv
dotenv_path = '.env'; load_dotenv(dotenv_path)
import twitter

tw_auth = twitter.OAuth(
  consumer_key=os.environ.get("TW_CONSUMER_KEY"),
  consumer_secret=os.environ.get("TW_CONSUMER_SECRET"),
  token=os.environ.get("TW_TOKEN"),
  token_secret=os.environ.get("TW_TOKEN_SECRET")
)

tw = twitter.Twitter(auth=tw_auth)
tw_userstream = twitter.TwitterStream(auth=tw_auth, domain='userstream.twitter.com')

# tweet the prediction of the number of RT when replied
from model.interface.rt_prediction import rt_prediction

for msg in twitter.userstream.user():
  if msg['in_reply_to_screen_name']=="TWITTER_ID":
    tweet = "@"+msg['user']['screen_name'] + " " + rt_prediction(msg["text"])
    tw.statuses.update(status=tweet)
