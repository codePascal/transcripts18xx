#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from transcripts18xx.postprocessing import TranscriptPostProcessor

from tests import context


class TestTranscriptPostProcessor1830(unittest.TestCase):

    def setUp(self) -> None:
        df = pd.read_csv(context.parsed_transcript_1830())
        self.tpp = TranscriptPostProcessor(df)

    def tearDown(self) -> None:
        self.tpp.save_to_dataframe(context.transcript_1830())

    def test_postprocessing(self):
        self.tpp.fill()
        self.tpp.add_states()
