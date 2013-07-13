#-*- coding: utf-8 -*-
import logging

import opml
import redis
from redis import Redis
from rq import Queue

from .config import config
from .database import db
from .feed import Feed
from .user import User


def fetch_feeds(user_id=None):
    query = Feed.query
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    for feed in query.all():
        add_feed_to_update_queue(feed)

def update_feed_wrapper(feed_id):
    db.init()
    Feed.query.get(feed_id).update()
    db.teardown()

def add_feed_to_update_queue(feed):
    # TODO: catch exception if redis is unavailable
    enqueue(update_feed_wrapper, feed.id)

def import_opml(user_id, url=None, data=None):
    outline = None
    if url is not None:
        outline = opml.parse(url)
    if data is not None:
        outline = opml.from_string(data)
    outline = outline or []
    for entry in outline:
        rss_url = entry.xmlUrl
        print rss_url
        feed = Feed(url=rss_url, user_id=user_id)
        db.session.add(feed)
        db.session.commit()
        feed.update()

def enqueue(func, *args):
    q = Queue(connection=Redis(**config.REDIS_CONNECTION_OPTIONS))
    try:
        j = q.enqueue(func, *args)
        print j
    except redis.exceptions.ConnectionError, e:
        logging.error('Redis connection error: %s', e)
