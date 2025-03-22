#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import passed


class TestPassActions(unittest.TestCase):

    def test_regular_pass(self):
        line = 'player1 passes'
        expected = {
            'action': 'Passed',
            'player': 'player1'
        }
        self.assertEqual(expected, passed.regular_pass(line))

    def test_no_valid_actions(self):
        line = 'player1 has no valid actions and passes'
        expected = {
            'action': 'Passed',
            'player': 'player1'
        }
        self.assertEqual(expected, passed.no_valid_actions(line))
