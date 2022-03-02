import tweepy as tpy
import not_important as passwords

tw_api_key = passwords.tw_api_key
tw_secret_key = passwords.tw_secret_key
tw_access_token = passwords.tw_access_token
tw_secret_token = passwords.tw_secret_token
bearer_token = passwords.bearer_token

auth = tpy.OAuthHandler(tw_api_key, tw_secret_key)
auth.set_access_token(tw_access_token, tw_secret_token)

api = tpy.API(auth)

def tweet(msg):
    api.update_status(msg)
    return

def get_timeline():
    timeline = api.home_timeline()
    tl_list = {}
    for tweet in timeline:
        tl_list[tweet.user.name] = tweet.text
    return tl_list