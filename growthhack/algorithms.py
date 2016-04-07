#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger 
from time import sleep, time

class TwitterAlgorithm(object):
  """All algorithms for twitter extend from this class"""

  def __init__(self, db, twitter, influx, options):
    self.l = getLogger(self.__class__.__name__)
    self.db = db 
    self.twitter = twitter
    self.influx = influx

    # reads the options in the sub classes
    self._read_options(options)

  def _read_options(self, options):
    """Reads in the options for the specific algorithm"""
    pass

  def run_once(self):
    """Runs the algorithm once, useful for sequential execution"""
    pass

class AutoUnfollow(TwitterAlgorithm):
  
  def _read_options(self, options):
    """Reads in the options for the specific algorithm"""
    pass

  def run_once(self):
    """Runs the algorithm once, useful for sequential execution"""
    twitter = self.twitter
    
    followers = twitter.get_followers()
    following = twitter.get_following()

    to_unfollow = filter(lambda x : x not in followers, following)
    for user_id in to_unfollow:
      twitter.unfollow_user(user_id)
      sleep(60)
    self.influx.write_unfollowing(len(to_unfollow))

class FollowBackAlgorithm(object):
  """FollowBackAlgorithm: Follows users from certain 
     topics, and waits for them to follow back. If they 
     do not follow back in a specified time interval; 
     then unfollow and put into blacklist"""

  def __init__(self, db, twitter, influx, options):
    self.l = getLogger("FollowBackAlgorithm")
    self.db = db 
    self.twitter = twitter
    self.influx = influx

    # options
    self.topics = options['topics']
    self.new_per_topic = options['new_per_topic']
    self.wait_for_follow = options['wait_for_follow']
    self.is_feasible = options['is_feasible']

    if(self.is_feasible == None):
      self.is_feasible_func = lambda x : True
    else: 
      self.is_feasible_func = lambda u : is_feasible(u)

  def get_not_followed_back(self, interval):
    l = self.l
    influx = self.influx

    followers = self.twitter.get_followers()
    influx.write_followers(len(followers))

    l.info("Followers %i" % len(followers))
    before = str(int(time()) - interval)
    followed = self.db.get_followed(before)
    m = "Testing %i followed before"
    l.info(m % len(followed))
    not_followed_back = []
    for user in followed:
      if(user not in followers):
        not_followed_back.append(user)
    return not_followed_back

  def run_once(self):
    l = self.l
    twitter = self.twitter
    influx = self.influx
    db = self.db

    # Getting following, for pushing stats to influx
    following = twitter.get_following()    
    influx.write_following(len(following))

    # Getting new followers
    for topic in self.topics:
      l.info("topic %s" % topic)

      cs = twitter.get_users_for_topic(topic)
      influx.write_fetched_tweets(len(cs))

      def uid(c,f): return f(c['id_str'])
      cs = filter(lambda x : uid(x, db.is_not_followed), cs)
      cs = filter(lambda x : uid(x, db.is_not_blacklisted), cs)
      cs = filter(self.is_feasible, cs)[:self.new_per_topic]

      m = "%i new feasible candidates"
      l.info(m % len(cs))

      for candidate in cs:
        twitter.follow_user(candidate['id_str'])
        db.insert_follow_user(candidate['id_str'])
        m = "follow user %s wait for follow back"
        l.info(m % candidate['screen_name'])
      influx.write_follows(len(cs))

    # Check if the followed follow back
    no_back_follow = \
      self.get_not_followed_back(self.wait_for_follow)
    m = "%i users did not follow back" 
    l.info(m % len(no_back_follow))
    influx.write_not_followed_back(len(no_back_follow))

    # Delete followed before
    before = str(int(time()) - self.wait_for_follow)
    followed = self.db.get_followed(before)
    for user in followed: 
      db.delete_follow_user(user)

    for user_id in no_back_follow:
      twitter.unfollow_user(user_id)
      m = "Unfollow user %s because no back follow"
      l.info(m % user_id)
      db.delete_follow_user(user_id)
      db.insert_blacklist(user_id)
      m = "Putting user %s into blacklist" 
      l.info(m % user_id)    

    influx.write_unfollowing(len(no_back_follow))
