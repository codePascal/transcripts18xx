#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx import games


class TestG18xx(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = games.Game18xx()


class TestG1830(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = games.Game1830()


class TestGames(unittest.TestCase):

    def test_argparse(self):
        self.assertEqual(games.Games.G1830, games.Games.argparse('G1830'))

        with self.assertRaises(ValueError):
            games.Games.argparse('g1830')

    def test_select(self):
        game = games.Games.G1830
        self.assertIsInstance(game.select(), games.Game1830)
