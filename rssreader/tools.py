#-*- coding: utf-8 -*-
import opml

from .extensions import db
from feed import Feed
from user import User
from rq import Queue
from redis import Redis


def fetch_feeds():
    for feed in Feed.query.all():
        enqueue(feed.update)

def update_feed(feed_id):
    with open('temp.txt', 'a') as f:
        print >>f, 'update feed {}'.format(feed_id)

def import_ompl():
    outline = opml.parse("rssreader/subscriptions.xml")
    for entry in outline:
        rss_url = entry.xmlUrl
        print rss_url
        user = User.query.filter_by(login='admin').first()
        feed = Feed(rss_url, user.get_id())
        db.session.add(feed)
        db.session.commit()
        feed.update()

def enqueue(func, *args):
    # TODO: add rq support
    q = Queue(connection=Redis())
    j = q.enqueue(func, *args)
    print j
