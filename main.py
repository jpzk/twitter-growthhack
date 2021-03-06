#!/usr/bin/env python
# -*- coding: utf-8 -*-

from growthhack.database import Database
from growthhack.twitter import TwitterClient
from growthhack.algorithms import * 
from growthhack.influx import InfluxWriter

from sys import argv
from logging import basicConfig, INFO
from time import sleep
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(argv[1])

## Options for FollowBackAlgorithm
def my_is_feasible(user):
  return ((user['followers_count'] < 1000) and \
  (user['lang'] == "en" or user['lang'] == "de"))

# Configuration version
configname = config.get('config','name')
version = config.get('config','version')
frequency = config.get('config', 'frequency')
configoptions = {'name': configname, 'version': version}

logfile = config.get('logging','filename')
twitter_options = {
      'consumer_key': config.get('twitter','consumer_key'),
      'consumer_secret':config.get('twitter','consumer_secret'),
      'access_token_key':config.get('twitter','access_token_key'),
      'access_token_secret':config.get('twitter','access_token_secret')
    }

db_options = {'database_file': config.get('db','file')}
influx_options = {
      'host': config.get('influxdb', 'host'),
      'port': int(config.get('influxdb', 'port')),
      'user': config.get('influxdb', 'user'),
      'password': config.get('influxdb', 'password'),
      'database': config.get('influxdb', 'database'),
      'config': configoptions, 
      'tables' : {
        'followers': config.get('influxdb', 'followers'),
        'unfollowing': config.get('influxdb', 'unfollowing'),
        'following': config.get('influxdb', 'following'),
        'follows': config.get('influxdb', 'follows'),
        'not_followed_back': config.get('influxdb', 'not_followed_back'),
        'fetched_tweets':config.get('influxdb', 'fetched_tweets')
      }
    }

topics = config.get('algorithm','topics').split(',')
algorithm_options = {
  'topics': topics,
  'config': configoptions,
  'follow_quota': int(config.get('algorithm','follow_quota')),
  'new_per_topic': int(config.get('algorithm','new_per_topic')),
  'wait_for_follow': int(config.get('algorithm','wait_for_follow')),
  'is_feasible':  my_is_feasible
}

db = Database(db_options)
twitter = TwitterClient(twitter_options)
influx = InfluxWriter(influx_options)
basicConfig(filename=logfile, level=INFO)

def main():
  fba = FollowBackAlgorithm(db, twitter, influx,algorithm_options)
  auf = AutoUnfollow(db, twitter, influx, algorithm_options) 
  
  while(True):
    fba.run_once()
    auf.run_once()
    sleep(frequency)

if __name__ == "__main__":
  main()

