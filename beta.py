import pandas as pd
import json
import requests
import warnings 
warnings.filterwarnings('ignore')

import time

## getting the tweets in English

df = pd.read_csv('tweets.csv')

df = df[['author_id', 'in_reply_to_user_id','created_at', 'text', 'lang', 'entities.mentions']]

df

eng_df = df.loc[df['lang']=='en']

eng_df

eng_df.text = eng_df.text.str.extract('(.*)@(.*)')[1].str.replace('elonmusk', '')

eng_df

eng_df.text = eng_df.text.str.replace(r'\n', ' ', regex = False)

eng_df

## parsing through the mentions on the tweets, converting the string objects into json format then getting the usernames
## also recording the unparsable object indexes for removal to ease the creation of the mentions column

mentions = []
missing = []

for no, element in  enumerate(eng_df['entities.mentions']):
    
    try: 
    
        json_object = json.loads(element)

        usernames = []
    
        for record in json_object: 

            usernames.append(record['username'])

        mentions.append(usernames)
        
    except:
        missing.append(no)
        pass
    
    
        ## creating a new index on the english dataframe then dropping the initial index
eng_df.reset_index(inplace = True)
eng_df.drop('index', axis = 1, inplace =True)

## dropping the records in the missing list. 
eng_df.drop(index = missing, inplace =True)

## creating a new index after dropping the missing records
eng_df.reset_index(inplace = True)

##removing the initial index
eng_df.drop('index', axis = 1, inplace =True)

## creating the mentions column

mentions_s = pd.Series(mentions)

eng_df = eng_df.assign(mentions = mentions_s)


## dropping the entites.mentions column
eng_df.drop('entities.mentions', axis =1, inplace = True)

## converting the created_at column to datetime
eng_df.created_at = pd.to_datetime(eng_df.created_at)

## clean dataframe containing the text of the tweets, author ids, reply_id and the mentions. 
eng_df

## getting the start and end time of the tweets
end_time = eng_df.created_at.max()

start_time = eng_df.created_at.min()

# fetching tesla stock data 
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=5min&outputsize=full&apikey=89RGQELIBJ0IF61Z'
r = requests.get(url)
data = r.json()


counter = 0

for k,v in data['Time Series (5min)'].items():
    
    data_dict = {}
    
    for key, value in v.items(): 
        
        data_dict[key[3:]] = float(value)
        
    ##creating a dataframe
    
    df = pd.DataFrame(data_dict, index=[0])
    
    df['Date'] = k
    
    if counter ==0: 
        
        total_df = df
        
        counter +=1
    
    else: 
        
        total_df = pd.concat([total_df, df])
    
    

total_df   

## getting Tesla stock dataframe
stock_df = total_df[['Date', 'open', 'high', 'low', 'close', 'volume']]

stock_df