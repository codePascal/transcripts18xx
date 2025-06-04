#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json
import os
import unittest.mock

import pandas as pd

from transcripts18xx import transcript

from tests import context


class TestTranscriptParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1830()
        tp = transcript.TranscriptParser(
            raw_transcript, transcript.games.Game1830()
        )
        tp.parse()
        os.remove(transcript.dataframe(raw_transcript))
        os.remove(transcript.metadata(raw_transcript))
        os.remove(transcript.states(raw_transcript))
        tp.save()
        cls.tp = tp

    def test_final_state_anonym(self):
        final_state = self.tp.final_state(anonym=True)
        self.assertIsInstance(final_state, dict)
        self.assertEqual(['players', 'companies'], list(final_state.keys()))
        self.assertEqual(
            {'player1', 'player2', 'player3', 'player4'},
            set(final_state['players'].keys())
        )
        self.assertEqual(
            self.tp._game.companies, set(final_state['companies'].keys())
        )

    def test_final_state_not_anonym(self):
        final_state = self.tp.final_state(anonym=False)
        self.assertIsInstance(final_state, dict)
        self.assertEqual(['players', 'companies'], list(final_state.keys()))
        self.assertEqual(
            {'mpcoyne', 'mpakfm', 'leesin', 'riverfiend'},
            set(final_state['players'].keys())
        )
        self.assertEqual(
            self.tp._game.companies, set(final_state['companies'].keys())
        )

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_verify_result_full(self, mock_stdout):
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
            "Full verification successful\n"
            "\n"
        )
        self.tp.verify_result(minimal=False)
        self.assertEqual(expected, mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_verify_result_minimal(self, mock_stdout):
        expected = str(
            "===================================\n"
            "State Differences: Parsed vs. Truth\n"
            "-----------------------------------\n"
            "-----------------------------------\n"
            "Minimal verification successful\n"
            "\n"
        )
        self.tp.verify_result(minimal=True)
        self.assertEqual(expected, mock_stdout.getvalue())

    def test_result(self):
        df = pd.read_csv(transcript.dataframe(context.transcript_1830()))
        # FIXME: results are not equal
        # self.assertTrue(df.equals(self.tp.result()))

    def test_metadata(self):
        with open(transcript.metadata(context.transcript_1830()), 'r') as f:
            metadata = json.load(f)
        self.assertEqual(
            {'game', 'id', 'num_players', 'players'}, set(metadata.keys())
        )
        self.assertEqual('1830', metadata['game'])
        self.assertEqual('201210', metadata['id'])
        self.assertEqual(4, metadata['num_players'])
        self.assertEqual(
            {
                'player1': 'mpcoyne',
                'player2': 'riverfiend',
                'player3': 'leesin',
                'player4': 'mpakfm'
            },
            metadata['players']
        )

    def test_final_states(self):
        with open(transcript.states(context.transcript_1830()), 'r') as f:
            states = json.load(f)
        self.assertEqual(states, self.tp.final_state(anonym=True))


class TestTranscriptRendering(unittest.TestCase):

    def test_dataframe_path(self):
        self.assertEqual(
            '1830_201210_final.csv',
            transcript.dataframe(context.transcript_1830()).relative_to(
                context._resources()).__str__()
        )

    def test_metadata_path(self):
        self.assertEqual(
            '1830_201210_metadata.json',
            transcript.metadata(context.transcript_1830()).relative_to(
                context._resources()).__str__()
        )

    def test_states_path(self):
        self.assertEqual(
            '1830_201210_states.json',
            transcript.states(context.transcript_1830()).relative_to(
                context._resources()).__str__()
        )

    def test_serialized_path(self):
        self.assertEqual(
            '1830_201210_serialized.json',
            transcript.serialized(context.transcript_1830()).relative_to(
                context._resources()).__str__()
        )

    def test_flattened_path(self):
        self.assertEqual(
            '1830_201210_flattened.csv',
            transcript.flattened(context.transcript_1830()).relative_to(
                context._resources()).__str__()
        )

    def test_serializing(self):
        serialized_data = transcript.serialize(context.transcript_1830())
        self.assertEqual(1346, len(serialized_data))
        self.assertIsInstance(serialized_data[0], dict)
        # TODO test

    def test_flatten(self):
        flattened_data = transcript.flatten(context.transcript_1830())
        self.assertEqual(1346, flattened_data.shape[0])
        # TODO test

    def test_transcript_name(self):
        # TODO test
        pass

    def test_transcript_id(self):
        # TODO test
        pass
