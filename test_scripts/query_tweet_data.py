#!/usr/bin/env python
#
#   query_tweet_data.py - program to get data for all of the tweet ids from the
#   twitter archive csv and image prediction tsv file. The tweet data will be
#   stored in separate files.
#
#   NOTE: I'm going to adapt this code to the wrangle_act notebook and then move
#   this file to the test_scripts dir so that it's no longer tracked by git.
#

import tweepy
import os
import sys
import pandas as pd
import json

import credentials as cred

# Declare list of file names and save directory
file_names = ['twitter_archive_tweet.txt',
              'image_prediction_tweet.txt']
save_dir = 'data'

# Check if dir and files exist and create them if they don't
if not os.path.exists('data'):
    os.mkdir(save_dir)

for file_name in file_names:
    file_path = os.path.join(save_dir, file_name)
    if not os.path.exists(file_path):
        os.mknod(file_path)

# Create tweepy api object
auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
auth.set_access_token(cred.access_token, cred.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if not api:
    print('Cant\'t authenticate')
    sys.exit(-1)

# Get the tweet ids
tweet_ids_all = []
# twitter_archive = pd.read_csv('data/twitter-archive-enhanced.csv')
# twitter_image_pred = pd.read_csv('data/image-predictions.tsv',
                                 # delim_whitespace=True)

tweet_ids_all.append(pd.read_csv('data/twitter-archive-enhanced.csv')
                       .tweet_id.astype(str).tolist())
tweet_ids_all.append(pd.read_csv('data/image-predictions.tsv',
                                 delim_whitespace=True)
                       .tweet_id.astype(str).tolist())

# Get all of the tweet data
for tweet_ids, file_name in zip(tweet_ids_all, file_names):
    file_path = os.path.join(save_dir, file_name)
    with open(file_path, 'w') as ofile:
        for tweet_id in tweet_ids:
            try:
                tweet_data = api.get_status(tweet_id, tweet_mode='extended')
            except tweepy.TweepError:
                pass
            else:
                ofile.write(json.dumps(tweet_data._json) + '\n')
                print('Retrieved data for tweet id: {}'.format(tweet_id))
    print('Retrieved data for all tweet ids.')
