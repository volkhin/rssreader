#!/usr/bin/env python
#-*- coding: utf-8 -*-

import opml
import feedparser

from .models import FeedEntry
from .extensions import db

def fetch_feeds():
    outline = opml.parse("rssreader/subscriptions.xml")
    for entry in outline:
        rss_url = entry.xmlUrl
        print rss_url
        data = feedparser.parse(rss_url)
        print data.version
        for entry in data.entries:
            title = entry.title
            content = entry.get('summary', '')
            for part in entry.get('content', []):
                content += part.value
            feed_entry = FeedEntry(title, content)
            db.session.add(feed_entry)
        db.session.commit()
