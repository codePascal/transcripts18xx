#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import unittest.mock
import pandas as pd

from transcripts18xx import transcript

from tests import context


class TestTranscriptParserG1830(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1830()
        tp = transcript.TranscriptParser(
            raw_transcript, transcript.games.Game1830()
        )
        tp.parse()
        cls.df = tp._df
        cls.metadata = tp._metadata

    def test_player_mapping(self):
        expected = {
            'mpcoyne': 'player1',
            'riverfiend': 'player2',
            'leesin': 'player3',
            'mpakfm': 'player4'
        }
        self.assertEqual(expected, self.metadata['mapping'])

    def test_anonymization_final_data(self):
        df = self.df.astype(str)
        self.assertFalse('leesin' in df.values)
        self.assertFalse('mpcoyne' in df.values)
        self.assertFalse('mpakfm' in df.values)
        self.assertFalse('riverfiend' in df.values)

    def test_last_state_evaluation(self):
        expected_finish = 'BankBroke'
        self.assertEqual(expected_finish, self.metadata['finished'])

        expected_result = {
            'player1': 6735,
            'player3': 6648,
            'player2': 5523,
            'player4': 2740
        }
        self.assertEqual(expected_result, self.metadata['result'])

        self.assertEqual('player1', self.metadata['winner'])

    def test_metadata(self):
        self.assertEqual('1830', self.metadata['game'])
        self.assertEqual('201210', self.metadata['id'])
        self.assertEqual(4, self.metadata['num_players'])


class TestTranscriptParserG1889(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1889()
        tp = transcript.TranscriptParser(
            raw_transcript, transcript.games.Game1889()
        )
        tp.parse()
        cls.df = tp._df
        cls.metadata = tp._metadata

    def test_player_mapping(self):
        expected = {
            'Sprint': 'player1',
            'Millie': 'player2',
            'zorbak': 'player3',
            'tado': 'player4',
            'mindbomb(UTC+9)': 'player5',
            'camping no reception': 'player6',
        }
        self.assertEqual(expected, self.metadata['mapping'])

    def test_anonymization_final_data(self):
        df = self.df.astype(str)
        self.assertFalse('Sprint' in df.values)
        self.assertFalse('Millie' in df.values)
        self.assertFalse('zorbak' in df.values)
        self.assertFalse('tado' in df.values)
        self.assertFalse('mindbomb(UTC+9)' in df.values)
        self.assertFalse('camping no reception' in df.values)

    def test_last_state_evaluation(self):
        expected_finish = 'BankBroke'
        self.assertEqual(expected_finish, self.metadata['finished'])

        expected_result = {
            'player1': 3968,
            'player2': 2468,
            'player3': 2804,
            'player4': 4249,
            'player5': 2807,
            'player6': 3775,
        }
        self.assertEqual(expected_result, self.metadata['result'])

        self.assertEqual('player4', self.metadata['winner'])

    def test_metadata(self):
        self.assertEqual('1889', self.metadata['game'])
        self.assertEqual('192767', self.metadata['id'])
        self.assertEqual(6, self.metadata['num_players'])

    # TODO: fix parsing G1889
    # @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    # def test_full_verification(self, mock_stdout):
    #     expected = str(
    #
    #     )
    #     ret = transcript.full_verification(context.transcript_1889())
    #     self.assertEqual(expected, mock_stdout.getvalue())
    #     self.assertTrue(ret)

    # def test_full_verification(self):
    #     self.assertTrue(transcript.full_verification(context.transcript_1889()))


class TestTranscriptContext(unittest.TestCase):

    def setUp(self) -> None:
        self.cnt = transcript.TranscriptContext.from_raw(
            context.transcript_1830()
        )

    def test_from_raw(self):
        self.assertEqual('1830_201210.txt', self.cnt.raw.name)
        self.assertEqual('1830_201210_metadata.json', self.cnt.meta_path.name)
        self.assertEqual('1830_201210_final.csv', self.cnt.result_path.name)
        self.assertEqual(201210, self.cnt.game_id)
        self.assertEqual('1830', self.cnt.game_type)
        self.assertTrue(self.cnt.valid)
        self.assertEqual('SUCCESS', self.cnt.parse_result)
        self.assertTrue(self.cnt.verification_result)
        self.assertEqual(4, self.cnt.num_players)
        self.assertEqual('BankBroke', self.cnt.game_ending)
        self.assertEqual('player1', self.cnt.winner)
        self.assertEqual([], self.cnt.unprocessed_lines)

    def test_metadata(self):
        metadata = self.cnt.metadata()
        self.assertIsInstance(metadata, dict)
        self.assertEqual(11, len(metadata.keys()))

    def test_result(self):
        df = self.cnt.result()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(1346, df.shape[0])
        self.assertEqual(165, df.shape[1])


class TestTranscriptVerification(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_full_verification(self, mock_stdout):
        expected = str(
            "===================================\n"
            "State Differences: Parsed vs. Truth\n"
            "-----------------------------------\n"
            "companies.B&M.tokens: '<missing>' != 0\n"
            "companies.B&O.tokens: '<missing>' != 1\n"
            "companies.C&O.tokens: '<missing>' != 0\n"
            "companies.CPR.tokens: '<missing>' != 3\n"
            "companies.ERIE.tokens: '<missing>' != 2\n"
            "companies.NYC.tokens: '<missing>' != 1\n"
            "companies.NYNH.tokens: '<missing>' != 0\n"
            "companies.PRR.tokens: '<missing>' != 0\n"
            "players.leesin.certs: '<missing>' != 23\n"
            "players.leesin.liquidity: '<missing>' != 5807\n"
            "players.mpakfm.certs: '<missing>' != 7\n"
            "players.mpakfm.liquidity: '<missing>' != 2610\n"
            "players.mpcoyne.certs: '<missing>' != 17\n"
            "players.mpcoyne.liquidity: '<missing>' != 6248\n"
            "players.riverfiend.certs: '<missing>' != 17\n"
            "players.riverfiend.liquidity: '<missing>' != 5142\n"
            "-----------------------------------\n"
        )
        ret = transcript.full_verification(context.transcript_1830())
        self.assertEqual(expected, mock_stdout.getvalue())
        self.assertTrue(ret)
