import pandas as pd
import numpy as np
import hvplot.pandas
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def generate_dummy_sentiments(stock_change_df):
    sentiment_df = stock_change_df.copy()
    num_rows = sentiment_df.shape[0]

    stock_change = stock_change_df.Close.values.reshape(-1, 1)
    noise = np.random.normal(0.01, 0.05, num_rows).reshape(-1, 1)

    dummy_sentiment = MinMaxScaler(feature_range=(-1, 1)).fit_transform(stock_change + noise)
    sentiment_df["Sentiment"] = dummy_sentiment
    sentiment_df.drop(columns='Close', inplace=True)

    return sentiment_df


def perform_analysis(twitter_handle, stock_ticker, analysis_date, dummy_sentiments=False):
    stock_csv = f"{stock_ticker}-{analysis_date}.csv"
    sentiment_csv = f"{twitter_handle}-{analysis_date}-sentiment.csv"

    stock_df = pd.read_csv(stock_csv, parse_dates=True, infer_datetime_format=True, index_col='Date')
    stock_change_df = stock_df.pct_change().dropna()

    if dummy_sentiments:
        sentiment_df = generate_dummy_sentiments(stock_change_df)
    else:
        sentiment_df = pd.read_csv(sentiment_csv, parse_dates=True, infer_datetime_format=True, index_col='Date')

    df = pd.concat([stock_change_df, sentiment_df], axis=1)
    print(df)
    print(df.corr())

    p = df.hvplot.line()
    hvplot.show(p)

if __name__ == "__main__":
    perform_analysis("elonmusk", "TSLA", dummy_sentiments=True)
