import sys
import questionary as q
import pandas as pd
import pandas_market_calendars as mcal

from sentiment import *
from analysis import *

'''
Retrieve user input for date of analysis
'''
def get_analysis_date():
    time_format = "%Y-%m-%d"

    # Allow date up to 2 years ago due to AlphaVantage API limits
    today = pd.Timestamp.today()
    start_date = (today - pd.Timedelta(730, "d")).strftime(time_format)
    end_date = today.strftime(time_format)

    # Using NYSE market calendar to filter for valid days that the stock market is open
    nyse_cal = mcal.get_calendar('NYSE')
    valid_nyse_days = nyse_cal.valid_days(start_date=start_date, end_date=end_date)

    # Retrieve user input with only valid NYSE days, with autocomplete
    analysis_date = q.autocomplete("Pick a valid stock market date (yyyy-MM-dd format) within the last 2 years for analysis:",
                                   choices=[d.strftime(time_format) for d in valid_nyse_days]).ask()

    return analysis_date

'''
Retrieve user input with questionary
'''
def user_input():
    print("Welcome to the twitter sentiment vs. stock price analysis tool!")

    # Get twitter handle of interest
    twitter_user = q.text("Please enter the twitter user handle of interest:").ask()
    # Get stock ticker of interest
    stock_ticker = q.text("Please enter the stock ticker of interest:").ask()
    stock_ticker = stock_ticker.upper()

    # Confirm user input
    confirmation = q.confirm(f"Do you want to proceed analysis for twitter user @{twitter_user} and stock ticker ^{stock_ticker}?").ask()

    if not confirmation:
        print("Ok! Exiting script...")
        sys.exit(0)

    # Get analysis date
    analysis_date = get_analysis_date()

    return twitter_user, stock_ticker, analysis_date


if __name__ == '__main__':
    twitter_user, stock_ticker, analysis_date = user_input()
    print(f"Analyzing twitter sentiment of @{twitter_user} against stock price of ^{stock_ticker} on {analysis_date}...")

    # Collect data and process

    # Perform sentiment analysis
    get_tweet_sentiment(twitter_user, analysis_date)

    # Perform correlation analysis
    perform_analysis(twitter_user, stock_ticker, analysis_date)
