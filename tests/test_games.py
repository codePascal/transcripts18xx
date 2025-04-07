#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx import games


class TestG18xx(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = games.Game18xx()

    def test_extract_pattern_event(self):
        line = 'player1 receives a 20% share of B&O'
        expected = dict(
            parent='Event',
            type='ReceiveShare',
            company='B&O',
            player='player1',
            percentage='20'
        )
        self.assertEqual(expected, self.cls.extract_pattern(line))

    def test_extract_pattern_action(self):
        line = 'B&O pays out $50 = $5 per share ($30 to player1, $5 to player2)'
        expected = dict(
            parent='Action',
            type='PayOut',
            company='B&O',
            amount='50',
            per_share='5',
        )
        self.assertEqual(expected, self.cls.extract_pattern(line))


class TestGames(unittest.TestCase):

    def test_argparse(self):
        self.assertEqual(games.Games.G1830, games.Games.argparse('G1830'))

        with self.assertRaises(ValueError):
            games.Games.argparse('g1830')

    def test_select(self):
        game = games.Games.G1830
        self.assertIsInstance(game.select(), games.Game1830)

