import datetime
import pandas as pd
import yfinance as yf
from pathlib import Path


def get_stock_data(stock_ticker, analysis_date):
    print(f"Fetching stock data for ^{stock_ticker} for {analysis_date}")
    stock_csv = f"^{stock_ticker}-{analysis_date}.csv"
    if Path(stock_csv).is_file():
        print(f"Skipping data fetching - file {stock_csv} exists")
        return

    start_date = datetime.datetime.strptime(analysis_date, "%Y-%m-%d")
    end_date = start_date + datetime.timedelta(days=1)
    df = yf.download(tickers=stock_ticker, start=analysis_date, end=end_date.strftime("%Y-%m-%d"), interval='5m')
    df.reset_index(inplace=True)
    df.drop(columns=['Open', 'High', 'Low', 'Close'], inplace=True)
    df.rename(columns={'Datetime': 'Date', 'Adj Close': 'Close'}, inplace=True)
    df.to_csv(stock_csv, index=False)


if __name__ == "__main__":
    get_stock_data("TSLA", "2022-10-05")
