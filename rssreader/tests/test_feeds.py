#-*- coding: utf-8 -*-
from ..feed import FeedEntry, Feed
from .common import TestCase


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
