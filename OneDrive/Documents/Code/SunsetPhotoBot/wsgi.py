import os
import praw
from time import time, sleep
from apscheduler.scheduler import Scheduler

 # set up bot scheduler
sched = Scheduler()
sched.start()

# Set REDDIT_USERNAME & REDDIT_PASSWORD enviro vars
# environment var example
# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# background task example
# https://devcenter.heroku.com/articles/python-rq

# Robot parameters
user_agent = ("SunsetPhotoBot .1 by /u/StringyLow")
post_limit = 100
sourceSub = 'BotTestingField'
targetSub = 'BotTestingField'
lastPostId = '' #get content more recent that this id
keywords = ['sunset', 'sun set', 'sunrise', 'sun rise']
allowedDomains = ['imgur.com']
already_done = []

def SunsetPhotoBot():
    # Login to Reddit.com
    bot = praw.Reddit(user_agent=user_agent)
    bot.login(REDDIT_USERNAME, REDDIT_PASSWORD)
    #bot.send_message('SunsetPhotoBot', 'Yo, gearhead', 'You are awesome!')

    # Scan the source sub-reddit and cross-post to target sub-reddit
    # while True:
    subreddit = bot.get_subreddit(sourceSub)
    for submission in subreddit.get_new(limit=post_limit):
        op_text = submission.title.lower()
        targetFound = any(string in op_text for string in keywords)
        # Test if title contains keywords
        if submission.domain in allowedDomains and targetFound and submission.id not in already_done:
            bot.submit(targetSub, submission.title, '', submission.url) # submit URL link
            already_done.append(submission.id)
            lastPostId = submission.id
            targetFound = False
 
sched.add_interval_job(SunsetPhotoBot, hours=1)
           
# required because this is a wsgi app
def application(environ, start_response):
    data = "Hello World!!!"
    start_response("200 OK", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(data)))
            ])
    return iter([data])

