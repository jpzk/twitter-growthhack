#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TwitterAPI import TwitterAPI
from time import sleep

class TwitterClient(object):
  """This class is used for the communication with the 
     Twitter API"""

  def __init__(self, options):
    self.api = TwitterAPI(\
          options['consumer_key'],\
          options['consumer_secret'],\
          options['access_token_key'],\
          options['access_token_secret'])

  def _sleep(self):
    sleep(5)

  def get_followers(self):
    followers = []
    for id in self.api.request('followers/ids'):
        followers.append(id)
    self._sleep()
    return followers
 
  def get_following(self):
    following = []
    for id in self.api.request('friends/ids'):
        following.append(id)
    self._sleep()
    return following

  def follow_user(self, user_id):
    r = self.api.request('friendships/create', {'user_id': user_id })
    if r.status_code == 200:
      status = r.json()
      print 'followed %s' % status['screen_name']
    self._sleep()

  def unfollow_user(self, user_id):
    r = self.api.request('friendships/destroy', {'user_id': user_id})
    if r.status_code == 200:
      status = r.json()
      print 'unfollowed %s' % status['screen_name']
    self._sleep()

  def get_users_for_topic(self, topic):
    r = self.api.request('search/tweets', {
      'count':200,
      'q':topic,
      'lang':"de"})
    statuses = r.json()['statuses']
    how_many = len(statuses)
    print("fetched " + str(how_many) + " tweets")
    self._sleep()

    users = map(lambda s : s['user'], statuses)
    users_id_unique = set()
    distinct = []
    for user in users:
      if(user['id_str'] not in users_id_unique):
        distinct.append(user)
        users_id_unique.add(user['id_str'])
    return distinct
  
