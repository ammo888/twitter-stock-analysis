import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
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
    print("Performing correlation analysis...")
    stock_csv = f"^{stock_ticker}-{analysis_date}.csv"
    sentiment_csv = f"@{twitter_handle}-{analysis_date}-sentiment.csv"

    stock_df = pd.read_csv(stock_csv, parse_dates=True, infer_datetime_format=True)
    stock_df['Date'] = pd.to_datetime(stock_df['Date'], infer_datetime_format=True)
    stock_df['Change'] = stock_df.Close.pct_change()
    stock_df.dropna(inplace=True)
    stock_df.set_index('Date', inplace=True)

    if dummy_sentiments:
        sentiment_df = generate_dummy_sentiments(stock_change_df)
    else:
        sentiment_df = pd.read_csv(sentiment_csv, parse_dates=True, infer_datetime_format=True)

    sentiment_df['timestamp'] = pd.to_datetime(sentiment_df['timestamp']).dt.round('5min')
    aggregated_sentiment_df = sentiment_df[['timestamp', 'weighted_sentiment', 'followers']].groupby('timestamp').agg(['sum', 'count'])
    aggregated_sentiment_df['final_sentiment'] = aggregated_sentiment_df['weighted_sentiment']['sum'] / aggregated_sentiment_df['followers']['sum']
    aggregated_sentiment_df['final_count'] = aggregated_sentiment_df['weighted_sentiment']['count']

    stock_plot = stock_df.Close.hvplot.line(title=f"^{stock_ticker} on {analysis_date}")
    stock_change_plot = stock_df.Change.hvplot.line(title=f"^{stock_ticker} % change on {analysis_date}")
    sentiment_plot = aggregated_sentiment_df.final_sentiment.hvplot.line(title=f"Aggregated sentiment for @{twitter_handle}")

    stock_plot_png = f"@{twitter_handle}-^{stock_ticker}-{analysis_date}.html"

    plot = hv.Layout(stock_plot + stock_change_plot + sentiment_plot).cols(1)

    hvplot.save(plot, stock_plot_png)

if __name__ == "__main__":
    perform_analysis("elonmusk", "TSLA", "2022-10-05")
