#-*- coding: utf-8 -*-
from flask.ext.testing import TestCase as Base

from .. import create_app, db
from ..config import config
from ..feed import FeedEntry, Feed
from ..user import User


class TestCase(Base):
    def create_app(self):
        config.set('testing')
        app = create_app()
        return app

    def _check_endpoint(self, endpoint):
        response = self.client.get(endpoint)
        self.assert200(response)
        return response

    def _login(self, login='admin', password='admin'):
        self.client.post('/login', data={'login': login, 'password': password})

    def _logout(self):
        self.client.get('/logout')

    def setUp(self):
        db.create_all()
        self._fill_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _fill_db(self):
        user = User(login='admin', password='admin')
        db.session.add(user)
        db.session.commit()
        feed = Feed(url='feed_url', user_id=user.id)
        db.session.add(feed)
        db.session.commit()
        entry1 = FeedEntry(url='test_url1', title='title1', content='content1', feed_id=feed.id)
        entry2 = FeedEntry(url='test_url2', title='title2', content='content2', feed_id=feed.id)
        db.session.add(entry1)
        db.session.add(entry2)
        db.session.commit()
