import praw
import requests


reddit = praw.Reddit(
    client_id=,
    client_secret=,
    password=,
    user_agent=,
    username=,
)


trigger_phrase = "and"
for comment in reddit.subreddit("learnpython+python").stream.comments():
  if trigger_phrase in comment.body.lower():
    print(comment.body)