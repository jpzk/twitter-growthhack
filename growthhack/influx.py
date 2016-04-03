#!/usr/bin/env python
# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient 
from datetime import datetime
from json import dumps

class InfluxWriter(object):
  """This class is used to interface the InfluxDB for 
     writing application internal metrics"""

  def __init__(self, options):
    self.host = options['host']
    self.port = options['port']
    self.user = options['user']
    self.password = options['password']
    self.database = options['database']
    self.config = options['config']

    def table(t): return options['tables'][t]
    self.followers = table('followers')
    self.following = table('following')
    self.follows = table('follows')
    self.not_followed_back = table('not_followed_back')
    self.fetched_tweets = table('fetched_tweets')

    self.client = InfluxDBClient(\
        self.host, self.port, self.user,
        self.password, database=self.database)
    self.client.switch_database(self.database)

  def _createPoint(self, name, value):
    return [{
      "measurement": name,
      "tags":{
          'config_name': self.config['name'],
          'config_version': self.config['version']
        },
      "fields": {"value": value}}]

  def _write_count(self, name, count):
    p = self._createPoint(name, count)
    result = self.client.write_points(p)

  def write_following(self, count):
    self._write_count(self.following, count)

  def write_followers(self, count):
    self._write_count(self.followers, count)

  def write_follows(self, count):
    self._write_count(self.follows, count)

  def write_not_followed_back(self, count):
    self._write_count(self.not_followed_back, count)

  def write_fetched_tweets(self, count):
    self._write_count(self.fetched_tweets, count)
 
