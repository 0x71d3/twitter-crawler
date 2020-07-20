import os
import random
import re
import string
import sys

import tweepy
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

sources = ['Twitter for Android', 'Twitter for iPhone', 'Twitter Web App']    

def filter_status(status):
    if 'http' in status.full_text:  # url
        return False
    if '#' in status.full_text:  # hashtag
        return False
    if set(status.full_text) - set(string.printable):  # string
        return False
    if len(status.full_text) <= 140:  # length
        return False
    return True

while True:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True)

    screen_names = set()
    for status in api.search(random.choice(string.ascii_letters),
            lang='en', result_type='recent', count=100, tweet_mode='extended'):
        if status.source in sources:
            screen_names.add(status.author.screen_name)
    # print(screen_names)

    id2status = {}

    in_reply_to_screen_names = set()
    for screen_name in screen_names:
        try:
            for status in api.user_timeline(screen_name,
                    count=200, tweet_mode='extended'):
                if filter_status(status):
                    id2status[status.id] = status
                    if (status.in_reply_to_screen_name is not None
                            and status.in_reply_to_screen_name not in screen_names):
                        in_reply_to_screen_names.add(status.in_reply_to_screen_name)
        except Exception as e:
            continue
    # print(in_reply_to_screen_names)

    for screen_name in in_reply_to_screen_names:
        try:
            for status in api.user_timeline(screen_name,
                    count=200, tweet_mode='extended'):
                if filter_status(status):
                    id2status[status.id] = status
        except Exception as e:
            continue
    # print(id2status)

    id2replyid = {}
    for status in id2status.values():
        if status.in_reply_to_status_id in id2status:
            id2replyid[status.in_reply_to_status_id] = status.id
    # print(id2replyid)

    with open('pairs.txt', 'a', encoding='utf-8') as f:
        for id_, replyid in id2replyid.items():
            tweet1 = id2status[id_].full_text.replace('\n', ' ')
            tweet1 = re.sub(r'@[0-9a-zA-Z_]{1,15} +', '', tweet1)

            tweet2 = id2status[replyid].full_text.replace('\n', ' ')
            tweet2 = re.sub(r'@[0-9a-zA-Z_]{1,15} +', '', tweet2)

            f.write(tweet1+ '\t' + tweet2 + '\n')
    print('Write ' + str(len(id2replyid)) + ' pairs.')
