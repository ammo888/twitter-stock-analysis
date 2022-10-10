

# Twitter Stock Analysis

## Project Overview
The premise of this project is to explore the relationship between twitter activity and a potentially related stock. Specifically, we aim to answer if #there is a lead-lag correlation between sentiment of twitter mentions of a user and some stock price. The end goal is a tool that takes in a twitter #handle, stock ticker, and day of interest, performs sentiment analysis on tweet mentions, and correlates aggregated sentiment against the stock price #movements.

## Limitations and Future Enhancements
Machine learning is a complex set of algorithms and functions that rely on clean and precise data inputs. We spend a lot of time cleaning and training data so that when input into a machine learning library or model, we get the output we are expecting. Twitter data is no exception to being problematic as an input into our spaCy models. Tweets can range from being concise professional language to slang and even other machine learning robots’ text that doesn't really resemble a coherent language. With this reality, We understand that there is a higher degree of noise in our ‘tweet’ data simply because of the nature of tweets and internet gargon.

Another limitation we faced when working on this project was the number of allowed tweets as well as the availabilty of twitter data fo revery corresponding stock price. There is much more consistnet and non-varying data when it comes to stock price data, compared to tweets. so, to combat this reality we broadned out resolution to aggregate tweets daily, insteal of 5 minutes or some other smaller time frame.

## Data Collection and Processing

Our team accessed stock data of TSLA from the twitter api using twarc2. Twarc2 is a great library that allows python to communicate with Twitter’s platform and consume its API, and from that you can extract information from Twitter. We were interested in the: number of followers, twitter handle, the actual tweet, and the timestamp. These were then put into a dataframe.

Twitter data is mostly unstructured, so the cleaning process involves removing emojis, special characters, and unnecessary blank spaces. Also includes removing duplicate tweets, making format adjustments, and getting rid of any missing data.

Once the data is gathered and sorted, it then needs to be cleaned before it can be used to train the Twitter sentiment analysis model. After gathering the data we had limitations on how many tweets we could pull at any given time due to our limitations set by the Twitter api. These limitations help twitter keep the usage under control and avoid congestion.

## Sentiment Analysis

We are using a machine learning tool called sentiment analysis in our project. This tool will analyze the text data that we feed it and compute a polarity metric which we will call a ‘sentiment score’. The main library used is called spaCy and the additional libraries (pipelines) are Asent, and SpacyTextBlob.

Spacy is a free open source library used for NLP (Natural Language Processing) and Asent and SpacyTextBlob are rule-based sentiment analysis tools which was developed on top of spaCy as the underlying library. These pipelines have additional features that can be used for further analytics, but we are just interested in the polarity.

Our goal in this module is to apply these pipelines to the twitter data and give every tweet a basic sentiment score that we will then correlate with the stock data.

- spaCy: https://spacy.io/

- Asent: https://github.com/kennethenevoldsen/asent

- SpacyTextBlob: https://github.com/sloria/TextBlob

## **Correlation Analysis**

Both the stock data and sentiment-analyzed tweet data is aggregated into 5 minute buckets
A cross-correlation between the two data sources is performed and produces a data on correlation between the two signals for every possible shift
For a stock x sentiment cross-correlation:
* If there’s peak correlation when the ‘lag’ is negative, then the sentiment signal leads the stock signal
* If there’s peak correlation when the ‘lag’ is positive, then the sentiment signal lags the stock signal

## **Driver Script**

`main.py` is the driver script that takes in the following user input:
Twitter handle
Stock ticker
Date of interest in the past two years (this limitation is due to AlphaVantage API limits) which is a valid NYSE trading day (we need stock price data)

The following procedures are performed in sequence from these files:
- `data.py` - data processing
- `sentiment.py` - sentiment analysis
- `analysis.py` - correlation analysis

Each of those steps are run independently of each other, requiring no explicit interaction between the methods. At the data processing step, caching based on existing CSV files is used. If there’s already stock price data for a given stock ticker and date in the directory, stock data fetching is skipped. Similarly, if twitter tweets for a given handle and date are present, fetching tweets is also skipped. For sentiment analysis, performing analysis is similarly skipped if the data exists. This caching is to avoid repeatedly invoking expensive and lengthy operations.


## **Setup**

Environment
```
$ conda create -n fintech python==3.7.2
$ conda activate fintech
$ pip install -r requirements.txt
```


Twitter API
Get twitter API access and put bearer token in a `.env` file in the repository root e.g.
BEARER_TOKEN=abcdefghijklmnop


Due to twitter API restrictions, it is advised to run `twitter.py` for an extended amount of time by editing the last line in the file for the desired twitter handle and date and running the following for as long as data is desired for:
$ watch -n240 twitter.py


Next, simply run the following
```
$ python main.py
```
