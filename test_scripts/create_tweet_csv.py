#!/usr/bin/env python
#
#   create_tweet_csv.py - program to create csv of extra tweet data for ease of
#   use in future analyses.
#
#   NOTE: I'm going to adapt the code to the wrangle_act ipython notebook and
#   then move this file to the test_scripts dir so that it's no longer tracked
#   by git.
#

import pandas as pd
import json
import os
import collections

# Load json objects one at a time and extract the necessary data from them
data_dir = 'data'
save_dir = 'test'
data_file_names = ['twitter_archive_tweet.txt', 'image_prediction_tweet.txt']
out_file_names = ['tweet_data-twitter_archive.csv',
                  'tweet_data-image_prediction.csv']
tweet_data = []
for data_file_name, out_file_name in zip(data_file_names, out_file_names):
    file_path_data = os.path.join(data_dir, data_file_name)
    with open(file_path_data) as data_file:
        for json_obj in data_file:
            tweet_data_sub = collections.OrderedDict()
            tweet_data_all = json.loads(json_obj)

            # Get all of the data we're interested in
            tweet_data_sub['id'] = tweet_data_all['id']
            tweet_data_sub['retweet_count'] = tweet_data_all['retweet_count']
            tweet_data_sub['favorite_count'] = tweet_data_all['favorite_count']
            tweet_data_sub['retweeted'] = tweet_data_all['retweeted']

            # Append it to the data gathering list
            tweet_data.append(tweet_data_sub)

    # Create a dataframe from the data and write it to a csv file
    file_path_csv = os.path.join(save_dir, out_file_name)
    pd.DataFrame(tweet_data).to_csv(file_path_csv, index=False)
