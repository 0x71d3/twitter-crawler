import argparse
import os
from datetime import datetime
from tqdm import tqdm

from dotenv import load_dotenv
import tweepy

sources = ['Twitter for Android', 'Twitter for iPhone', 'Twitter Web App']

parser = argparse.ArgumentParser()
parser.add_argument('output_dir')
args = parser.parse_args()

load_dotenv()

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

while True:
    user_ids = set()

    search_results = api.search(q='い', lang='ja', result_type='recent', count=100, tweet_mode='extended')
    for status in tqdm(search_results):
        if status.source in sources:
            user_ids.add(status.author.id)

    in_reply_to_user_ids = set()

    status_id_to_full_text = {}
    status_id_to_user_id = {}

    status_id_to_in_reply_to_status_id = {}

    for user_id in tqdm(user_ids):
        try:
            user_timeline = api.user_timeline(user_id=user_id, count=200, tweet_mode='extended')
            for status in user_timeline:
                if status.source not in sources:
                    continue

                if len(status.entities['hashtags']) > 0 or 'media' in status.entities or len(status.entities['urls']) > 0:
                    continue
                
                status_id_to_full_text[status.id] = ' '.join(status.full_text.split())
                status_id_to_user_id[status.id] = status.author.id

                if status.in_reply_to_user_id is not None:
                    in_reply_to_user_ids.add(status.in_reply_to_user_id)
                    status_id_to_in_reply_to_status_id[status.id] = status.in_reply_to_status_id

        except tweepy.TweepError:
            pass

    for in_reply_to_user_id in tqdm(in_reply_to_user_ids - user_ids):
        try:
            user_timeline = api.user_timeline(user_id=in_reply_to_user_id, count=200, tweet_mode='extended')
            for status in user_timeline:
                if status.source not in sources:
                    continue

                if len(status.entities['hashtags']) > 0 or 'media' in status.entities or len(status.entities['urls']) > 0:
                    continue

                status_id_to_full_text[status.id] = ' '.join(status.full_text.split())
                status_id_to_user_id[status.id] = status.author.id

                if status.in_reply_to_status_id is not None:
                    status_id_to_in_reply_to_status_id[status.id] = status.in_reply_to_status_id

        except tweepy.TweepError:
            pass

    dialogues = []

    for status_id in tqdm(set(status_id_to_in_reply_to_status_id.keys()) - set(status_id_to_in_reply_to_status_id.values())):  # is leaf
        full_texts = []
        user_ids = []

        while True:
            if status_id not in status_id_to_full_text.keys():  # continues
                break

            full_texts.append(status_id_to_full_text[status_id])
            user_ids.append(status_id_to_user_id[status_id])

            if status_id not in status_id_to_in_reply_to_status_id.keys():  # is root
                if len(full_texts) >= 2 and len(set(user_ids)) == 2 and len(set(user_ids[0::2])) == 1 and len(set(user_ids[1::2])) == 1:
                    dialogues.append(reversed(full_texts))
                
                break

            status_id = status_id_to_in_reply_to_status_id[status_id]
        
    with open(os.path.join(args.output_dir, f'{datetime.now():%Y%m%d%H%M%S%f}.tsv'), 'w', encoding='utf-8') as f:
        for dialogue in dialogues:
            f.write('\t'.join(dialogue) + '\n')

    print(f'{len(dialogues)} dialogues written')
