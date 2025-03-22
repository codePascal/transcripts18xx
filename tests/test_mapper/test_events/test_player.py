#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.events import player


class TestPlayerEvents(unittest.TestCase):

    def test_becomes_president(self):
        line = 'player1 becomes the president of B&O'
        expected = {
            'event': player.PlayerEvents.PresidentNomination.name,
            'player': 'player1',
            'company': 'B&O'
        }
        self.assertEqual(expected, player.becomes_president(line))

    def test_has_priority_deal(self):
        line = 'player1 has priority deal'
        expected = {
            'event': player.PlayerEvents.PriorityDeal.name,
            'player': 'player1'
        }
        self.assertEqual(expected, player.has_priority_deal(line))

    def test_operates_company(self):
        line = 'player1 operates B&O'
        expected = {
            'event': player.PlayerEvents.OperatesCompany.name,
            'player': 'player1',
            'company': 'B&O'
        }
        self.assertEqual(expected, player.operates_company(line))
