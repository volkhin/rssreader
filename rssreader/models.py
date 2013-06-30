#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sqlalchemy as db
from database import Base

class FeedEntry(Base):
    __tablename__ = 'feed_entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<FeedEntry {}>'.format(self.title)

class Feed(Base):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    title = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(256))
    password = db.Column(db.String(256))
    feeds = db.relationship('Feed', backref='user', lazy='dynamic')
