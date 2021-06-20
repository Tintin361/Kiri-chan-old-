import praw
import random
import not_important

CLIENT_ID = not_important.client_id
CLIENT_SECRET = not_important.client_secret
PASSWORD = not_important.reddit_password

reddit = praw.Reddit(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  user_agent="discord:kirlia-chan-bot:v0.4.10 (by /u/tintin361yt)",
  username="Kirlia-chan",
  password=PASSWORD)
  
def last_post(sub):
  subreddit = reddit.subreddit(sub)
  
  for submission in subreddit.new(limit=1):
    title = submission.title
    url = submission.url
    sub_title = subreddit.display_name
    
  return title, url, sub_title
  
def hot_post(sub):
  subreddit = reddit.subreddit(sub)
  stop_number = random.randint(0, 100)
  i = 0
  
  for submission in subreddit.hot(limit=100):
    title = submission.title
    url = submission.url
    sub_title = subreddit.display_name
    i = i + 1
    if i == stop_number:
      return title, url, sub_title

def fake_history():
  subreddit = reddit.subreddit("fakehistoryporn")
  stop_number = random.randint(0, 100)
  i = 0

  for submission in subreddit.hot(limit=1000):
    title = submission.title
    url = submission.url
    i = i + 1
    if i == stop_number:
      return title, url
