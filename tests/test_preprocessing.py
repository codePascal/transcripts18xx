#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.preprocessing import GameTranscriptProcessor
from transcripts18xx.games import g1830

from tests import context


class TestGameTranscriptProcessor1817(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class TestGameTranscriptProcessor1830(unittest.TestCase):

    def setUp(self) -> None:
        gtp = GameTranscriptProcessor(
            context.transcript_1830(), g1830.Game1830()
        )
        gtp.parse_transcript()
        self.df = gtp.save_to_dataframe()

    def tearDown(self) -> None:
        pass

    def test_shape(self):
        self.assertEqual(1346, self.df.shape[0])
        self.assertEqual(23, self.df.shape[1])
