import asent
import numpy as np
import pandas as pd
import spacy
from datetime import datetime
from pathlib import Path
from spacytextblob.spacytextblob import SpacyTextBlob


def get_tweet_sentiment(twitter_user, analysis_date, custom_tweets_file=None):
    print("Gathering sentiment from your selection...")

    tweets_file_csv = f"@{twitter_user}-{analysis_date}.csv" if custom_tweets_file is None else custom_tweets_file
    sentiment_file_csv = f"@{twitter_user}-{analysis_date}-sentiment.csv"

    if Path(sentiment_file_csv).is_file():
        print(f"Skipping sentiment analysis - file {sentiment_file_csv} exists")
        return

    try:
        f = open(tweets_file_csv)
        f.close()

    except FileNotFoundError:
        print("File not found. FileNotFoundError occured.")
        exit(1)

    tweet_df = pd.read_csv(tweets_file_csv, infer_datetime_format=True, parse_dates=True)
    tweet_df.dropna(inplace=True)

    # Temporary bandaid for followers count
    tweet_df["followers"] = np.random.randint(1, high=1_000_000, size=tweet_df.shape[0])

    # Adding spacy model and the sentencizer and asent pipelines

    nlp = spacy.load('en_core_web_lg')
    nlp.add_pipe('sentencizer')
    nlp.add_pipe('asent_en_v1')
    nlp.add_pipe('spacytextblob')

    tweet_df["sentiment_asent"] = tweet_df["text"].apply(lambda tweet: nlp(tweet)._.polarity.compound)
    tweet_df['sentiment_textblob'] = tweet_df["text"].apply(lambda tweet: nlp(tweet)._.blob.polarity)
    tweet_df['average_sentiment'] = tweet_df[["sentiment_asent", "sentiment_textblob"]].mean(axis=1)

    # tweet_weighted_sentiment = followers * average_sentiment

    tweet_df['weighted_sentiment'] = tweet_df["average_sentiment"] * tweet_df["followers"]
    tweet_df.to_csv(sentiment_file_csv, index=False)

if __name__ == '__main__':
    get_tweet_sentiment("elonmusk", "2022-10-05")
