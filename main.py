import sys
import questionary as q


def user_input():
    print("Welcome to the twitter sentiment vs. stock price analysis tool!")

    twitter_user = q.text("Please enter the twitter user handle of interest:").ask()
    stock_ticker = q.text("Please enter the stock ticker of interest:").ask()
    stock_ticker = stock_ticker.upper()

    confirmation = q.confirm(f"Do you want to proceed analysis for twitter user @{twitter_user} and stock ticker ^{stock_ticker}?").ask()

    if not confirmation:
        print("Ok! Exiting script...")
        sys.exit(0)

    return twitter_user, stock_ticker


if __name__ == '__main__':
    twitter_user, stock_ticker = user_input()
    print(f"Analyzing twitter sentiment of @{twitter_user} against stock price of ^{stock_ticker}...")

