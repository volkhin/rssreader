#-*- coding: utf-8 -*-
import feedparser
from bleach import clean

from ..extensions import db


class FeedEntry(db.Model):
    __tablename__ = 'feed_entries'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), index=True, unique=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))

    def __init__(self, url, title, content, feed):
        self.url = url
        self.title = title
        self.content = content
        self.feed = feed

    def __repr__(self):
        return '<FeedEntry {}>'.format(self.id)


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    title = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    entries = db.relationship('FeedEntry', backref='feed', lazy='dynamic')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id

    def update(self):
        data = feedparser.parse(self.url)
        for entry in data.entries:
            url = entry.link
            title = entry.title
            content = entry.get('summary', '')
            for part in entry.get('content', []):
                content += part.value
            content = clean(content, ['br', 'p', 'em', 'h1', 'h2'], strip=True)
            content = u'<div>{}</div>'.format(content)
            result = FeedEntry.query.filter_by(url=url).scalar()
            if not result:
                feed_entry = FeedEntry(url, title, content, self)
                db.session.add(feed_entry)
        db.session.commit()
