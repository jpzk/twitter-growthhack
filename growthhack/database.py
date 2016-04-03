#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect
from time import time

DATABASE_FILE = "growthhack.db"
TEST_QUERY = "SELECT * FROM followed LIMIT 1"
CREATE_TABLE = "CREATE TABLE followed (date int, user text)"
CREATE_BLACKLIST = "CREATE TABLE blacklist (user text)"
INSERT_FOLLOWER = "INSERT INTO followed VALUES ('%s', '%s')"
INSERT_BLACKLIST = "INSERT INTO blacklist VALUES ('%s')"
DELETE_FOLLOWER = "DELETE FROM followed WHERE user = '%s'"
SELECT_FOLLOWED = "SELECT user FROM followed WHERE date < %s"
IS_FOLLOWED = "SELECT user FROM followed WHERE user = '%s'"
IS_BLACKLISTED = "SELECT user FROM blacklist WHERE user = '%s'"

class Database(object):
  def __init__(self, options):
    self.conn = connect(options['database_file'])
    self.create_schema()

  def create_schema(self):
    """Create the domain model schema, this should be done
       better, not using exception for table exist checking"""

    conn = self.conn
    c = conn.cursor()
    def create_tables(conn, c): 
      c.execute(CREATE_TABLE)
      c.execute(CREATE_BLACKLIST)
      conn.commit()
    try:
      c.execute(TEST_QUERY)
      conn.commit()
    except: 
      print "creating table followed, blacklist"
      create_tables(conn, c)

  def insert_blacklist(self, user):
    """Insert a record into black list"""
    conn = self.conn
    c = conn.cursor()
    c.execute(INSERT_BLACKLIST % user)
    conn.commit()

  def is_not_blacklisted(self, user_id):
    """Select is user is already followed"""
    conn = self.conn
    c = conn.cursor()
    result = []
    for r in c.execute(IS_BLACKLISTED % user_id):
      result.append(r)
    return len(result) < 1

  def insert_follow_user(self, user_id):
    """Insert a record for following a user"""
    conn = self.conn
    c = conn.cursor()
    t = str(int(time()))
    data = (t, user_id)
    c.execute(INSERT_FOLLOWER % data)
    conn.commit()

  def delete_follow_user(self, user_id):
    """Delete a record for following a user"""
    conn = self.conn
    c = conn.cursor()
    c.execute(DELETE_FOLLOWER % user_id)
    conn.commit()

  def is_not_followed(self, user_id):
    """Select is user is already followed"""
    conn = self.conn
    c = conn.cursor()
    result = []
    for r in c.execute(IS_FOLLOWED % user_id):
      result.append(r)
    return len(result) < 1

  def get_followed(self, before):
    """Check if the followed user followed back"""
    c = self.conn.cursor()
    check_followers = []
    print before
    for user in c.execute(SELECT_FOLLOWED % before):
      check_followers.append(user)
    return check_followers 

