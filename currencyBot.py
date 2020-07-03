# -*- coding: utf-8 -*-

import tweepy
from datetime import datetime
import time
import praw
import requests
import pprint
import json

with open('auth.json') as f:
    datastore = json.load(f)


url = 'https://prime.exchangerate-api.com/v5/9926f025c5c6faa8cae5397f/latest/USD'

lastData = '0.00'

reddit = praw.Reddit(client_id=datastore[0]['client_id'],
                     client_secret=datastore[0]['client_secret'],
                     user_agent=datastore[0]['user_agent'])

consumer_key = datastore[0]['consumer_key']
consumer_secret = datastore[0]['consumer_secret']

access_token = datastore[0]['access_token']
access_token_secret = datastore[0]['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for submission in reddit.subreddit("starterpacks").hot(limit=10):
    print(submission.title)

print (reddit.read_only)
# print(dataUSD['conversion_rates']['BRL'])


while (True):
    responseUSD = requests.get(url)
    dataUSD = responseUSD.json()
    actualData = str(dataUSD['conversion_rates']['BRL'])
    print (actualData)

    if(lastData != actualData):
        now = datetime.now()
        currentTime = now.strftime("%H:%M:%S")
        if(actualData < lastData):
            api.update_status(
                currentTime + "\n Dólar caiu :(  \nR$ " + actualData)
        else:
            api.update_status(
                currentTime + "\nDólar subiu :)  \nR$ " + actualData)

        print('twittou')
        lastData = actualData
    time.sleep(3600)
