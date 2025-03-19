#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.patterns import events


class TestEventsPattern(unittest.TestCase):

    def test_trains_rust(self):
        line = '-- Event: 2 trains rust'
        ret = events.trains_rust(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Train Rust', ret['event'])
        self.assertEqual('2', ret['train'])

    def test_trains_are_obsolete(self):
        line = '-- Event: 2+ trains are obsolete'
        ret = events.trains_are_obsolete(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Train Obsolete', ret['event'])
        self.assertEqual('2+', ret['train'])

    def test_train_exports(self):
        line = '-- Event: A 4 train exports'
        ret = events.train_exports(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Train Export', ret['event'])
        self.assertEqual('4', ret['train'])

    def test_obsolete_trains_rust(self):
        line = '-- Event: Obsolete trains rust'
        ret = events.obsolete_trains_rust(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Obsolete Train Rust', ret['event'])

    def test_private_companies_close(self):
        line = '-- Event: Private companies close'
        ret = events.private_companies_close(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Private Companies Close', ret['event'])

    def test_game_over(self):
        line = '-- Game over:'
        ret = events.game_over(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Game Over', ret['event'])
