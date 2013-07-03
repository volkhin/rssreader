#-*- coding: utf-8 -*-
from flask.ext.login import UserMixin

from ..database import db


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
