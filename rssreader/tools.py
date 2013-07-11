#-*- coding: utf-8 -*-
import opml
from redis import Redis
from rq import Queue

from .config import config
from .database import db
from .feed import Feed
from .user import User


def fetch_feeds():
    for feed in Feed.query.all():
        add_feed_to_update_queue(feed)

def update_feed_wrapper(feed_id):
    db.init()
    Feed.query.get(feed_id).update()
    db.teardown()

def add_feed_to_update_queue(feed):
    enqueue(update_feed_wrapper, feed.id)

def import_ompl():
    outline = opml.parse("rssreader/subscriptions.xml")
    for entry in outline:
        rss_url = entry.xmlUrl
        print rss_url
        user = User.query.filter_by(login='admin').first()
        feed = Feed(url=rss_url, user_id=user.get_id())
        db.session.add(feed)
        db.session.commit()
        feed.update()

def enqueue(func, *args):
    q = Queue(connection=Redis(**config.REDIS_CONNECTION_OPTIONS))
    j = q.enqueue(func, *args)
    print j
