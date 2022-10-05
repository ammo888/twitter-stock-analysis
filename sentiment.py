import asent
import hvplot as hv
import numpy as np
import pandas as pd
import spacy
from datetime import datetime
from dframcy import dframcy
from spacytextblob.spacytextblob import SpacyTextBlob


def get_tweet_sentiment(twitter_user, analysis_date):
    print("Gathering sentiment from your selection...")

    tweets_file_csv = f"{twitter_user}-{analysis_date}.csv"
    sentiment_file_csv = f"{twitter_user}-{analysis_date}-sentiment.csv"

    try:
        f = open(tweets_file_csv)
        f.close()

    except FileNotFoundError:
        print("File not found. FileNotFoundError occured.")
        exit(1)

    tweet_df = pd.read_csv(tweets_file_csv, index_col="date", infer_datetime_format=True, parse_dates=True)
    tweet_df.dropna(inplace=True)

    # Adding spacy model and the sentencizer and asent pipelines

    nlp = spacy.blank('en')
    nlp.add_pipe('sentencizer')
    nlp.add_pipe('asent_en_v1')

    tweet_df["sentiment_asent"] = tweet_df["tweet"].apply(lambda tweet: nlp(tweet)._.polarity.compound)

    nlp2 = spacy.load('en_core_web_sm')
    nlp2.add_pipe('spacytextblob')
    nlp2

    tweet_df['sentiment_textblob'] = tweet_df['tweet'].apply(lambda tweet: nlp2(tweet)._.blob.polarity)

    tweet_df['average_sentiment'] = tweet_df[["sentiment_asent", "sentiment_textblob"]].mean(axis=1)

    # weighted score = followers * sentiment score + followers * sentiment score / total number of followers

    tweet_df['weighted_sentiment'] = (tweet_df["followers"])*(tweet_df["average_sentiment"]).sum()/tweet_df["followers"].sum()

    output_file = tweet_df.to_csv(sentiment_file_csv, index = True)
    print('\nCSV String:\n', output_file)
