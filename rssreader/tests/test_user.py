#-*- coding: utf-8 -*-
from flask import json
from .common import TestCase

class TestUser(TestCase):
    def test_index(self):
        response = self._check_endpoint('/api/1/settings')
        self.assertTrue('error' in response.data)
        self.assertTrue('password' not in response.data)
        self._login()
        response = self._check_endpoint('/api/1/settings')
        self.assertTrue('error' not in response.data)

    def test_update(self):
        self._login()
        response = self._check_endpoint('/api/1/settings')
        obj = json.loads(response.data)
        self.assertFalse(obj['show_read'])
        obj['show_read'] = True
        response2 = self.client.put('/api/1/settings', data=json.dumps(obj))
        self.assert200(response2)
        response3 = self._check_endpoint('/api/1/settings')
        obj2 = json.loads(response3.data)
        self.assertTrue(obj2['show_read'])
