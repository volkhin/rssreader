#-*- coding: utf-8 -*-
import datetime

import feedparser
from bleach import clean

from ..database import db


class FeedEntry(db.Model):
    __tablename__ = 'feed_entries'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), index=True, unique=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    created_at = db.Column(db.DateTime)
    read = db.Column(db.Boolean, default=False)

    def __init__(self, url, title, content, feed, created_at):
        self.url = url
        self.title = title
        self.content = content
        self.feed = feed
        self.created_at = created_at

    def __repr__(self):
        return '<FeedEntry {}>'.format(self.id)

    def mark_read(self):
        self.read = True
        db.session.commit()

    def mark_unread(self):
        self.read = False
        db.session.commit()


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    title = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    entries = db.relationship('FeedEntry', backref=db.backref('feed'), lazy='dynamic')
    unread_count = db.Column(db.Integer, default=0)

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id

    def get_title(self):
        return self.title or self.url

    def update(self):
        def clean_text(text):
            tags = ['img', 'br', 'p', 'em', 'h1', 'h2']
            attrs = {
                    'img': ['src', 'alt'],
                    }
            return clean(text, tags, attrs, strip=True)

        data = feedparser.parse(self.url)
        self.title = data.feed.title
        for entry in data.entries:
            url = entry.link
            title = entry.title
            created_at = datetime.datetime(*entry.published_parsed[0:6])
            content = entry.get('summary', '')
            if 'content' in entry.keys():
                content = ''
                for part in entry['content']:
                    content += part.value
            content = clean_text(content)
            content = u'<div>{}</div>'.format(content)
            result = FeedEntry.query.filter_by(url=url).scalar()
            if not result:
                feed_entry = FeedEntry(url, title, content, self, created_at)
                db.session.add(feed_entry)
        db.session.commit()

    def get_entries_count(self):
        return self.entries.count()

    def get_unread_entries_count(self):
        return self.entries.filter_by(read=False).count()
