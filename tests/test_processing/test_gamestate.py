#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from transcripts18xx.processing.gamestate import GameStateProcessor
from transcripts18xx.games import Game1830

from tests import context


class TestGameStateProcessor1830(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        df = pd.read_csv(context.processed_transcript_1830())
        gsp = GameStateProcessor(df, Game1830())
        gsp.generate()
        cls.df = gsp.save_to_dataframe(context.transcript_1830())

    def test(self):
        # TODO: add tests
        pass
