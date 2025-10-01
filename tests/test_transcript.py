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
        self.assertFalse(
            df.apply(lambda x: x.str.contains('leesin')).any().any()
        )
        self.assertFalse(
            df.apply(lambda x: x.str.contains('mpcoyne')).any().any()
        )
        self.assertFalse(
            df.apply(lambda x: x.str.contains('mpakfm')).any().any()
        )
        self.assertFalse(
            df.apply(lambda x: x.str.contains('riverfiend')).any().any()
        )

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
        self.assertFalse(
            df.apply(lambda x: x.str.contains('Sprint')).any().any()
        )
        self.assertFalse(
            df.apply(lambda x: x.str.contains('Millie')).any().any()
        )
        self.assertFalse(
            df.apply(lambda x: x.str.contains('zorbak')).any().any()
        )
        self.assertFalse(
            df.apply(lambda x: x.str.contains('tado')).any().any()
        )
        self.assertFalse(
            df.apply(lambda x: x.str.contains('mindbomb(UTC+9)')).any().any()
        )
        self.assertFalse(
            df.apply(
                lambda x: x.str.contains('camping no reception')
            ).any().any()
        )

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


class TestTranscriptRendering(unittest.TestCase):

    def test_dataframe_path(self):
        self.assertEqual(
            '1830_201210_final.csv',
            transcript.dataframe_path(
                context.transcript_1830()).relative_to(
                context._resources()).__str__()
        )

    def test_dataframe(self):
        df = transcript.dataframe(context.transcript_1830())
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(1346, df.shape[0])
        self.assertEqual(165, df.shape[1])

    def test_metadata_path(self):
        self.assertEqual(
            '1830_201210_metadata.json',
            transcript.metadata_path(context.transcript_1830()).relative_to(
                context._resources()).__str__()
        )

    def test_metadata(self):
        metadata = transcript.metadata(context.transcript_1830())
        self.assertIsInstance(metadata, dict)
        self.assertEqual(11, len(metadata.keys()))

    def test_num_players(self):
        self.assertEqual(4, transcript.num_players({'num_players': 4}))
        self.assertIsNone(transcript.num_players({}))

    def test_game_ending(self):
        self.assertEqual(
            'NotFinished', transcript.game_ending({'finished': 'NotFinished'}))

        self.assertIsNone(transcript.game_ending({}))

    def test_verification_result(self):
        self.assertFalse(
            transcript.verification_result({'verification': {'success': False}})
        )
        self.assertTrue(
            transcript.verification_result({'verification': {'success': True}})
        )
        self.assertIsNone(transcript.verification_result({'verification': {}}))
        self.assertIsNone(transcript.verification_result({}))

    def test_parse_result(self):
        self.assertEqual(
            'SUCCESS', transcript.parse_result({'parse_result': 'SUCCESS'})
        )
        self.assertIsNone(transcript.parse_result({}))

    def test_valid_record(self):
        self.assertTrue(
            transcript.valid_record(
                {'verification': {'success': True}, 'parse_result': 'SUCCESS'}
            )
        )
        self.assertFalse(
            transcript.valid_record(
                {'verification': {'success': False}, 'parse_result': 'SUCCESS'}
            )
        )
        self.assertFalse(
            transcript.valid_record(
                {'verification': {'success': True}, 'parse_result': ''}
            )
        )
        self.assertFalse(transcript.valid_record({}))

    def test_transcript_name(self):
        self.assertEqual(
            '1830_123456', transcript.transcript_name('1830_123456_final.csv')
        )
        self.assertEqual(
            '1830_12345', transcript.transcript_name('1830_12345_metadata.json')
        )

    def test_transcript_id(self):
        self.assertEqual(
            '123456', transcript.transcript_id('1830_123456_final.csv')
        )
        self.assertEqual(
            '12345', transcript.transcript_id('1830_12345_metadata.json')
        )

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
