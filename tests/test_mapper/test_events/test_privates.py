#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.events import privates


class TestPrivatesEvents(unittest.TestCase):

    def test_all_close(self):
        line = '-- Event: Private companies close'
        expected = {
            'event': 'AllPrivatesClose',
        }
        self.assertEqual(expected, privates.all_close(line))

    def test_closes(self):
        line = 'Mohawk & Hudson closes'
        expected = {
            'event': 'PrivateCloses',
            'private': 'Mohawk & Hudson'
        }
        self.assertEqual(expected, privates.closes(line))

    def test_is_auctioned(self):
        line = 'Mohawk & Hudson goes up for auction'
        expected = {
            'event': 'PrivateAuction',
            'private': 'Mohawk & Hudson'
        }
        self.assertEqual(expected, privates.is_auctioned(line))
