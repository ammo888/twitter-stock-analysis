import asent
import numpy as np
import pandas as pd
import spacy
from datetime import datetime
from pathlib import Path
from spacytextblob.spacytextblob import SpacyTextBlob

'''
Sentiment analysis on tweets
'''
def get_tweet_sentiment(twitter_user, analysis_date, custom_tweets_file=None, use_large_model=True):
    print("Gathering sentiment from your selection...")

    tweets_file_csv = f"@{twitter_user}-{analysis_date}.csv" if custom_tweets_file is None else custom_tweets_file
    sentiment_file_csv = f"@{twitter_user}-{analysis_date}-sentiment.csv"

    # Skip analysis if already done
    if Path(sentiment_file_csv).is_file():
        print(f"Skipping sentiment analysis - file {sentiment_file_csv} exists")
        return

    try:
        f = open(tweets_file_csv)
        f.close()

    except FileNotFoundError:
        print("File not found. FileNotFoundError occured.")
        exit(1)

    # Read in tweets
    tweet_df = pd.read_csv(tweets_file_csv, infer_datetime_format=True, parse_dates=True)
    tweet_df.dropna(inplace=True)

    # Choose which spacy model to use - en_core_web_lg is larger, slower, but better statistically
    spacy_model = 'en_core_web_lg' if use_large_model else 'en_core_web_sm'

    # Adding spacy model and the sentencizer and asent/textblob pipelines
    nlp = spacy.load(spacy_model)
    nlp.add_pipe('sentencizer')
    nlp.add_pipe('asent_en_v1')
    nlp.add_pipe('spacytextblob')

    # Calculate sentiments for tweets and retrieve scores
    tweet_sentiments = list(nlp.pipe(tweet_df.text))
    tweet_df["sentiment_asent"] = [tweet_nlp._.polarity.compound for tweet_nlp in tweet_sentiments]
    tweet_df['sentiment_textblob'] = [tweet_nlp._.blob.polarity for tweet_nlp in tweet_sentiments]
    tweet_df['average_sentiment'] = tweet_df[["sentiment_asent", "sentiment_textblob"]].mean(axis=1)

    # Calculate weighted sentiment = average sentiment * num followers
    tweet_df['weighted_sentiment'] = tweet_df["average_sentiment"] * tweet_df["followers"]
    tweet_df.to_csv(sentiment_file_csv, index=False)

if __name__ == '__main__':
    get_tweet_sentiment("elonmusk", "2022-10-05")
