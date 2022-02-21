import praw
import random
import not_important

CLIENT_ID = not_important.client_id
CLIENT_SECRET = not_important.client_secret
PASSWORD = not_important.reddit_password

reddit = praw.Reddit(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  user_agent="discord.py:kirlia-chan-bot:v1.2.3 (by u/tintin361yt)",
  username="Kirlia-chan",
  password=PASSWORD,
  check_for_async=False)
  
def last_post(sub):
  subreddit = reddit.subreddit(sub)
  
  for submission in subreddit.new(limit=1):
    title = submission.title
    url = submission.url
    sub_title = subreddit.display_name
    id = submission.id
    author = submission.author

    if submission.over_18:
      nsfw = "True"
    else:
      nsfw = "False"
    
  return title, url, sub_title, id, nsfw, author
  
def hot_post(sub):
  subreddit = reddit.subreddit(sub)
  stop_number = random.randint(0, 100)
  i = 0
  
  for submission in subreddit.hot(limit=100):
    title = submission.title
    url = submission.url
    sub_title = subreddit.display_name
    id = subreddit.id
    author = submission.author

    i = i + 1
    if i == stop_number:
      if submission.over_18:
        nsfw = "True"
      else:
        nsfw = "False"

      return title, url, sub_title, id, nsfw, author

def get(sub, last_rad):
  subreddit = reddit.subreddit(sub)
  stop_number = random.randint(0, last_rad)
  i = 0

  for submission in subreddit.hot(limit=1000):
    title = submission.title
    url = submission.url
    id = submission.id
    author = submission.author

    if submission.over_18:
      nsfw = "True"
    else:
      nsfw = "False"

    i = i + 1
    if i == stop_number:
      return title, url, id, nsfw, author

def upvote(post):
  submission = reddit.submission(id=post)
  try:
    submission.upvote()
  except:
    return "False"
  return score(post)

def score(post):
  sub = reddit.submission(id=post)
  try:
    score = sub.score
    return str(score)
  except:
    return "Null"