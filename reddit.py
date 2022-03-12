import praw
import random
import not_important
from discord.embeds import Embed

CLIENT_ID = not_important.client_id
CLIENT_SECRET = not_important.client_secret
PASSWORD = not_important.reddit_password

reddit = praw.Reddit(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  user_agent="discord.py:kirlia-chan-bot:v1.2.7 (by u/tintin361yt)",
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

def get_comments(post):
  post = reddit.submission(id=post)
  post.comment_sort = "new"
  top_com = list(post.comments)
  print(top_com)
  
  long_top_com = len(top_com)
  if long_top_com <= 0:
    return False
  elif long_top_com < 6:
    leng = long_top_com
  else:
    leng = 6
  
  message = Embed(title="Commentaires les plus récents:", description="", color=0xff4300)
  for i in range (0, leng):
    p = reddit.submission(id=top_com[i])
    message.add_field(name=f"Commentaire de :{p.author}", value=p.title, inline=False)
    
  return message