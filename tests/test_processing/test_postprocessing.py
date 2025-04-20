#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from transcripts18xx.processing.postprocessing import TranscriptPostProcessor
from transcripts18xx.games import Game1830

from tests import context


class TestTranscriptPostProcessor1830(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        df = pd.read_csv(context.parsed_transcript_1830())
        tpp = TranscriptPostProcessor(df, Game1830())
        df = tpp.process()
        filepath = context.transcript_1830().parent.joinpath(
            context.transcript_1830().stem + '_processed.csv'
        )
        df.to_csv(filepath, index=False, sep=',')
        cls.df = df

    @staticmethod
    def _set_not_nan(ser: pd.Series) -> set:
        return set(ser.dropna().unique())

    def _type_int(self, ser: pd.Series) -> bool:
        return any(float(s).is_integer() for s in self._set_not_nan(ser))

    def test_shape(self):
        self.assertEqual(1346, self.df.shape[0])
        self.assertEqual(21, self.df.shape[1])

    def test_columns(self):
        expected = [
            'amount', 'company', 'direction', 'id', 'location', 'new_train',
            'old_train', 'parent', 'per_share', 'percentage', 'phase', 'player',
            'private', 'rotation', 'route', 'sequence', 'share_price', 'source',
            'tile', 'train', 'type'
        ]
        self.assertEqual(sorted(expected), sorted(list(self.df.columns)))

    def test_phase(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, set(self.df.phase.unique()))

    def test_company(self):
        expected = {
            'B&M', 'CPR', 'NYC', 'NYNH', 'ERIE', 'C&O', 'B&O', 'PRR'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.company))

    def test_player(self):
        expected = {'player1', 'player2', 'player3', 'player4'}
        self.assertEqual(expected, self._set_not_nan(self.df.player))

    def test_sequence(self):
        expected = {
            'ISR 1',
            'OR 1.1',
            'OR 2.1',
            'OR 3.1',
            'OR 4.1', 'OR 4.2',
            'OR 5.1', 'OR 5.2',
            'OR 6.1', 'OR 6.2', 'OR 6.3',
            'OR 7.1', 'OR 7.2', 'OR 7.3',
            'OR 8.1', 'OR 8.2', 'OR 8.3',
            'SR 1', 'SR 2', 'SR 3', 'SR 4', 'SR 5', 'SR 6', 'SR 7', 'SR 8'
        }
        self.assertEqual(expected, set(self.df.sequence.unique()))

    def test_location(self):
        expected = {
            'A19', 'B10', 'B12', 'B14', 'B16', 'B18', 'B20', 'B22', 'C11',
            'C13', 'C17', 'C9', 'D10', 'D12', 'D16', 'D18', 'D20', 'D8', 'E11',
            'E13', 'E19', 'E21', 'E23', 'F10', 'F12', 'F14', 'F16', 'F18',
            'F20', 'F22', 'F6', 'G13', 'G15', 'G17', 'G19', 'G3', 'G5', 'G7',
            'G9', 'H10', 'H12', 'H14', 'H16', 'H18', 'H4', 'H6', 'H8', 'I15',
            'I17'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.location))

    def test_source(self):
        expected = {
            'Auction', 'B&M', 'Baltimore & Ohio', 'Camden & Amboy',
            'Champlain & St.Lawrence', 'Delaware & Hudson', 'ERIE', 'IPO',
            'Mohawk & Hudson', 'NYNH', 'Schuylkill Valley', 'The Depot',
            'market', 'player1', 'player2', 'player3'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.source))

    def test_anonymization(self):
        df = self.df.astype(str)
        for col in df.columns:
            for p in ['leesin', 'mpakfm', 'riverfiend', 'mpcoyne']:
                self.assertFalse(df[col].str.contains(p).any())
