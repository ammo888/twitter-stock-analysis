import pandas as pd
import requests
import warnings
warnings.filterwarnings('ignore')
import datetime
import csv




def fetch_stock_data(ticker, year, month):

    '''

    :param ticker: stock market symbol for the target company
    :param year: could either be 1 or 2, 1 represents current year, 2 represents previous year
    :param month: 1-12 representing each month in a year.
    :return: Dataframe containing Open, High, Low , closing stock prices and the volume traded
    '''
    ## getting current month
    current_month = datetime.datetime.now().date().month
    prev_month = current_month - 1

    if (year == 1 and month < prev_month) or (year == 2):

        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        CSV_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year{year}month{month}&apikey=89RGQELIBJ0IF61Z'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            df = pd.DataFrame(data=my_list[1:], columns=my_list[0])

        ## converting time into datetime
        df['time'] = pd.to_datetime(df['time'], utc=True)

        ##renaming time column to Date
        df.rename(columns={'time': 'Date'}, inplace=True)

        total_df = df.copy()

        return total_df


    else:

        # fetching tesla stock data
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=5min&outputsize=full&apikey=89RGQELIBJ0IF61Z'
        r = requests.get(url)
        data = r.json()

        ## parsing the TSLA stock data and creating a dataframe with all the stock information

        counter = 0

        for k, v in data['Time Series (5min)'].items():

            data_dict = {}

            for key, value in v.items():
                data_dict[key[3:]] = float(value)

            ##creating a dataframe

            df = pd.DataFrame(data_dict, index=[0])

            df['Date'] = k

            if counter == 0:

                total_df = df

                counter += 1

            else:

                total_df = pd.concat([total_df, df])

            ## getting Tesla stock dataframe and filtering the data to get only 5min data between the time periods in the tweets data frame.
            total_df = total_df[['Date', 'open', 'high', 'low', 'close', 'volume']]

        return total_df


