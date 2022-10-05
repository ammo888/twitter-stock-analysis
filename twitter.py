import os
import json
import itertools
import datetime
import pytz
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from twarc.client2 import Twarc2
from twarc.expansions import ensure_flattened

load_dotenv()

bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# App Auth - bearer token
t = Twarc2(bearer_token=bearer_token)

# App Auth - consumer key + secret
# t = Twarc2(consumer_key=consumer_key, consumer_secret=consumer_secret)

# User Auth - consumer key + secret and access token + secret
# t = Twarc2(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)


def user_lookup(twitter_handle):
    resp = t.user_lookup([twitter_handle], usernames=True)
    return int(next(resp)["data"][0]["id"])


def search_date(analysis_date):
    time_format = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(analysis_date, time_format)

    tz = pytz.timezone("US/Eastern")
    start_date = tz.localize(start_date).astimezone(pytz.utc)
    end_date = start_date + datetime.timedelta(days=1)

    return start_date, end_date


def mentions(user_id, start_date, end_date, num_tweets=5, num_pages=1):
    print(f"Retreiving mentions for {user_id} from {start_date} to {end_date}")
    resp = t.mentions(user_id, tweet_fields=['created_at'], max_results=num_tweets, start_time=start_date, end_time=end_date)

    df = pd.DataFrame(columns=['id', 'author_id', 'author', 'timestamp', 'text'])

    for _ in range(num_pages):
        try:
            r = next(resp)
        except StopIteration:
            break

        for tweet in ensure_flattened(r):
            df = df.append({
                'id': tweet['id'],
                'author_id': tweet['author_id'],
                'author': tweet['author']['username'],
                'timestamp': tweet['created_at'],
                'text': tweet['text']
            }, ignore_index=True)

    return df


def get_tweets(twitter_handle, analysis_date, num_tweets=50, num_pages=16, append=True):
    print(f"Fetching tweets for @{twitter_handle} for {analysis_date} with {num_pages} pages with up to {num_tweets} tweets per page")

    tweets_file_csv = f"@{twitter_handle}-{analysis_date}.csv"

    existing_tweets_df = None
    if append and Path(tweets_file_csv).is_file():
        print(f"Loading exists tweets from {tweets_file_csv}")
        existing_tweets_df = pd.read_csv(tweets_file_csv, infer_datetime_format=True, parse_dates=True)

    user_id = user_lookup(twitter_handle)
    print(f"User id for {twitter_handle} is {user_id}")

    start_date, end_date = search_date(analysis_date)

    if existing_tweets_df is not None:
        start_date = existing_tweets_df.timestamp.max()

    twitter_df = mentions(user_id, start_date, end_date, num_tweets=num_tweets, num_pages=num_pages)
    print(f"Fetched data contains {twitter_df.shape[0]} tweets")

    if existing_tweets_df is not None:
        twitter_df = twitter_df.append(existing_tweets_df, ignore_index=True)
        print(f"Total data contains {twitter_df.shape[0]} tweets")
    twitter_df.to_csv(tweets_file_csv, index=False)

if __name__ == "__main__":
    get_tweets("elonmusk", "2022-10-05", num_tweets=50, num_pages=16, append=True)
