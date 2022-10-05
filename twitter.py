import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')


def getting_mention_df(csv_file ,mention):

    '''

    :param csv_file: location of the csv file
    :param mention: Mention to be found on tweet text
    :return: dataframe containing relevant useful information about the tweet, the author and follower count
    '''

    df = pd.read_csv(csv_file)

    df = df[['author_id', 'in_reply_to_user_id' ,'created_at', 'text', 'lang', 'entities.mentions', 'author.public_metrics.followers_count']]

    df.rename(columns = {'author.public_metrics.followers_count': 'followers'}, inplace =True)

    ## getting the tweets in English

    eng_df = df.loc[df['lang' ]=='en']

    ## getting the tweets that contain the mention specified

    eng_df = eng_df[eng_df['text'].str.contains(mention)]

    ## removing Elon musk tag
    eng_df.text = eng_df.text.str.extract('(.*)@(.*)')[1].str.replace('elonmusk', '')

    eng_df.text = eng_df.text.str.replace(r'\n', ' ', regex = False)

    # parsing through the mentions on the tweets, converting the string objects into json format then getting the usernames
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

    return eng_df

## Example
##print(getting_mention_df("tweets.csv", "tesla"))
