#-*- coding: utf-8 -*-
import opml

from .extensions import db
from feed import Feed
from user import User


def fetch_feeds():
    for feed in Feed.query.all():
        feed.update()

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
