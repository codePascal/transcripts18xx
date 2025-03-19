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
        self.gtp = GameTranscriptProcessor(
            context.transcript_1830(), g1830.Game1830())

    def tearDown(self) -> None:
        pass

    def test_processor(self):
        self.gtp.parse_transcript()
        self.gtp.save_to_dataframe()
