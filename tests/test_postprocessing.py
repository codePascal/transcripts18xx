#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from transcripts18xx.postprocessing import TranscriptPostProcessor
from transcripts18xx.games import Game1830

from tests import context


class TestTranscriptPostProcessor1830(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        df = pd.read_csv(context.parsed_transcript_1830())
        tpp = TranscriptPostProcessor(df, Game1830())
        tpp.process()
        cls.df = tpp.save_to_dataframe(context.transcript_1830())

    def test(self):
        # TODO: add tests
        pass
