import praw
import requests


reddit = praw.Reddit(
    client_id="-vo1jgs5tX0-BojGtt6TYg",
    client_secret="MI5FfQKYlqcTIQAo9OdxegOMLzji4A",
    password="65CA!5K2AGB-U.",
    user_agent="firstBot",
    username="hanni777",
)


trigger_phrase = "and"
for comment in reddit.subreddit("learnpython+python").stream.comments():
  if trigger_phrase in comment.body.lower():
    print(comment.body)