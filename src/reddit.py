import praw
import pandas as pd
import os
from dotenv import load_dotenv
from prawcore.exceptions import Forbidden

load_dotenv()
client_id=os.getenv('REDDIT_CLIENT_ID')
client_secret=os.getenv('REDDIT_SECRET')
user_agent=os.getenv('REDDIT_USER_AGENT')

reddit_read_only = praw.Reddit(client_id = client_id, 
                            client_secret = client_secret, 
                            user_agent = user_agent)

class RedditHandler:

    def __init__(self, subreddit):
        self.subreddit_name = subreddit
        self.subreddit = reddit_read_only.subreddit(str(self.subreddit_name))
        self.newest_post_title = ""

    def changeSubreddit(self, newsub):
        self.subreddit_name = newsub
    
    def getTopFive(self):
        posts = []
        for post in self.subreddit.hot(limit=5):
            posts.append(post)
        return posts
    
    def getNewFive(self):
        for post in self.subreddit.new(limit=5):
            print(post.title)
            print(post.url)
            print("==================")

    def getNewestPost(self):
        for post in self.subreddit.new(limit=1):
            if post.title != self.newest_post_title:
                return post.url


