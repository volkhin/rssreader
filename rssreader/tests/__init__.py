#!/usr/bin/env python
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
        user = User('admin', 'admin')
        db.session.add(user)
        feed = Feed('feed_url', user.id)
        entry1 = FeedEntry('test_url1', 'title1', 'content1', feed, None)
        entry2 = FeedEntry('test_url2', 'title2', 'content2', feed, None)
        db.session.add(feed)
        db.session.add(entry1)
        db.session.add(entry2)
        db.session.commit()


class TestFeeds(TestCase):
    def test_index(self):
        response = self.client.get('/feeds')
        self.assert_redirects(response, '/login?next=%2Ffeeds')
        self._login()
        response = self.client.get('/feeds')
        self.assert200(response)
        self.assertTrue('All items' in self._check_endpoint('/feeds').data)
        self.assert404(self.client.get('/feeds234'))
        self._logout()
        response = self.client.get('/feeds')
        self.assert_redirects(response, '/login?next=%2Ffeeds')

    def test_mark_read(self):
        unread_entries_number = FeedEntry.query.filter_by(read=False).count()
        entry = FeedEntry.query.filter_by(read=False).first()
        entry.mark_read()
        self.assertEqual(FeedEntry.query.filter_by(read=False).count(),
                unread_entries_number - 1)
        self.client.post('/api/1/mark_entry_unread', data={'entry_id': entry.id})
        self.assertEqual(FeedEntry.query.filter_by(read=False).count(),
                unread_entries_number - 1)
        self._login()
        self.client.post('/api/1/mark_entry_unread', data={'entry_id': entry.id})
        self.assertEqual(FeedEntry.query.filter_by(read=False).count(),
                unread_entries_number)
