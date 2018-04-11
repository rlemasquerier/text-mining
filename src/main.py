# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 09:56:36 2018

@author: Rodolphe
"""

import tweepy #Twitter API
import json #JSon data files management
from nltk.tokenize import TweetTokenizer 
from tweepy import OAuthHandler

from nltk.corpus import stopwords
import string

import collections

import vincent

# import API Keys 
import config

def load_online_data():
    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET
    access_token = config.ACCESS_TOKEN
    access_secret = config.ACCESS_SECRET
     
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
     
    api = tweepy.API(auth)
        
    query = '#RUSFRA -filter:retweets'
    max_tweets = 200
        
    with open('airfrance.json', 'w') as f:
        for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
            # Process a single status
            # Add one jyson dict per line to read easily later
            json.dump(status._json,f)
            f.write('\n')
            
def load_first_line():
    with open('airfrance.json', 'r') as f:
        line = f.readline() # read only the first tweet/line
        tweet = json.loads(line) # load it as Python dict
        #print(json.dumps(tweet, indent=4)) # pretty-print
        return tweet
    
def load_and_tokenize():
    with open('airfrance.json','r') as f:
        res = []
        tknzr = TweetTokenizer(preserve_case=False)
        for line in f:
            tweet = json.loads(line)
            res.append(tknzr.tokenize(tweet['text']))
        return res
    
def word_occurences(data):
    #Define stopwords
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + stopwords.words('french') 
    stop += ['les']
    stop += punctuation 
    stop += ['rt', 'via']
    stop += list(string.ascii_letters)
    stop += ['...','…',"'",'’']
    count_all = collections.Counter()
    count_all.update([word for tweet in tweets for word in tweet if word not in stop])
    return count_all.most_common(25)
    
            
if __name__ == '__main__':
    load_online_data()
    tweets = load_and_tokenize()
    top_occurences = word_occurences(tweets)
    labels, freq = zip(*top_occurences)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    #rotate x axis labels
    ax = vincent.AxisProperties(labels = vincent.PropertySet(angle=vincent.ValueRef(value=90)))
    bar.axes[0].properties = ax
    #Export visu to JSON file
    bar.to_json('term_freq.json')
    

    