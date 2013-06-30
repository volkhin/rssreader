#!/usr/bin/env python
#-*- coding: utf-8 -*-

from flask.ext.login import UserMixin
from .extensions import db

class FeedEntry(db.Model):
    __tablename__ = 'feed_entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<FeedEntry {}>'.format(self.title)

class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    title = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(256))
    password = db.Column(db.String(256))
    feeds = db.relationship('Feed', backref='user', lazy='dynamic')

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def check_password(self, password):
        return self.password == password

    @classmethod
    def authenticate(cls, login, password):
        user = User.query.filter(User.login == login).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

