#-*- coding: utf-8 -*-
from flask import json
from ..feed import FeedEntry, Feed
from .common import TestCase


class TestFeeds(TestCase):
    def test_login_logout(self):
        response = self._check_endpoint('/api/1/feeds')
        self.assertTrue('error' in response.data)
        self._login()
        response = self._check_endpoint('/api/1/feeds')
        self.assertTrue('error' not in response.data)
        self._logout()
        response = self._check_endpoint('/api/1/feeds')
        self.assertTrue('error' in response.data)

    def test_index(self):
        self._login()
        response = self._check_endpoint('/api/1/feeds')
        self.assertTrue('feed_url' in response.data)

    def test_mark_read(self):
        response = self._check_endpoint('/api/1/entries')
        self.assertTrue('error' in response.data)
        self._login()
        response = self._check_endpoint('/api/1/entries')
        self.assertTrue('error' not in response.data)
        entries = json.loads(response.data)
        unread_entries_number = FeedEntry.query.filter_by(read=False).count()
        self.assertTrue(unread_entries_number == 2)
        entries[0]['read'] = True
        response = self.client.put('/api/1/entries/{}'.format(entries[0]['id']),
                data=json.dumps(entries[0]))
        self.assert200(response)
        unread_entries_number = FeedEntry.query.filter_by(read=False).count()
        self.assertTrue(unread_entries_number == 1)
