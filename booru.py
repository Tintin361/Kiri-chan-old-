# Unfinished
from pybooru import Moebooru

safe = Moebooru('safebooru')

def search_safebooru(search):
    posts = safe.post_list(search)
    return posts.last_call