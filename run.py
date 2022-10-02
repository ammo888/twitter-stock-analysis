import numpy as np
import pandas as pd
from datetime import datetime
import hvplot as hv
import spacy
import asent
from dframcy import dframcy
from spacytextblob.spacytextblob import SpacyTextBlob
import sys
import questionary as q
import pandas_market_calendars as mcal


def get_analysis_date():
    time_format = "%Y-%m-%d"
    nyse_cal = mcal.get_calendar('NYSE')

    today = pd.Timestamp.today()
    start_date = (today - pd.Timedelta(730, "d")).strftime(time_format)
    end_date = today.strftime(time_format)

    valid_nyse_days = nyse_cal.valid_days(start_date=start_date, end_date=end_date)

    analysis_date = q.autocomplete("Pick a stock market date (yyyy-MM-dd format) within the last 2 years for analysis:",
                                   choices=[d.strftime(time_format) for d in valid_nyse_days]).ask()

    return analysis_date


def user_input():
    print("Welcome to the twitter sentiment vs. stock price analysis tool!")

    twitter_user = q.text("Please enter the twitter user handle of interest:").ask()
    stock_ticker = q.text("Please enter the stock ticker of interest:").ask()
    stock_ticker = stock_ticker.upper()

    confirmation = q.confirm(f"Do you want to proceed analysis for twitter user @{twitter_user} and stock ticker ^{stock_ticker}?").ask()

    if not confirmation:
        print("Ok! Exiting script...")
        sys.exit(0)

    analysis_date = get_analysis_date()

    return twitter_user, stock_ticker, analysis_date


if __name__ == '__main__':
    twitter_user, stock_ticker, analysis_date = user_input()
    print(f"Analyzing twitter sentiment of @{twitter_user} against stock price of ^{stock_ticker} on {analysis_date}...")
