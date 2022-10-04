import sys
import questionary as q
import pandas as pd
import pandas_market_calendars as mcal
import numpy as np
from datetime import datetime
import hvplot as hv
import spacy
import asent
from dframcy import dframcy
from spacytextblob.spacytextblob import SpacyTextBlob

def get_tweet_sentiment(username):
    print("Gathering Senitment from your selection...")

    try:
        f = open(f"{username}.csv")
        f.close()
 
    except FileNotFoundError:
        print("File not found. FileNotFoundError occured.")
    
    tweet_df = pd.read_csv(f"{username}.csv", index_col="date", infer_datetime_format=True, parse_dates=True)
    tweet_df.dropna(inplace=True)

# Adding spacy model and the sentencizer and asent pipelines

    nlp = spacy.blank('en')
    nlp.add_pipe('sentencizer')
    nlp.add_pipe('asent_en_v1')

    tweet_df["Sentiment_asent"] = tweet_df["tweet"].apply(lambda tweet: nlp(tweet)._.polarity.compound)

    nlp2 = spacy.load('en_core_web_sm')
    nlp2.add_pipe('spacytextblob')
    nlp2

    tweet_df['Sentiment_textblob'] = tweet_df['tweet'].apply(lambda tweet: nlp2(tweet)._.blob.polarity)
    
    tweet_df['average_sentiment'] = tweet_df[["Sentiment_asent", "Sentiment_textblob"]].mean(axis=1)

# weighted score = followers * sentiment score + followers * sentiment score / total number of followers

    tweet_df['weighted_sentiment'] = (tweet_df["followers"])*(tweet_df["average_sentiment"]).sum()/tweet_df["followers"].sum()

    output_file = df.to_csv(f'{username}_sentiment.csv', index = True)
    print('\nCSV String:\n', output_file)
   
    return tweet_df