#!/usr/bin/env python
#-*- coding: utf-8 -*-

from flask import Flask, render_template
import opml
import feedparser

from database import db_session, init_db
from .models import FeedEntry, Feed, User

from .extensions import db

ALL = ['create_app']

def fetch_feeds():
    outline = opml.parse("subscriptions.xml")
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
            db_session.add(feed_entry)
        db_session.commit()

@app.route('/')
def index():
    # fetch_feeds()
    entries = FeedEntry.query.all()
    return render_template('index.html', entries=entries)
    output = '<br/>'.join(entry.title for entry in entries)
    return output

def create_app():
    app = Flask(__name__, static_folder='static')
    db.init_app(app)
    app.config.from_object(__name__)
    return app

if __name__ == "__main__":
    app = create_app()
    init_db()
    app.run(debug=True)

