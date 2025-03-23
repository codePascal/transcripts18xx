#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from transcripts18xx.preprocessing import GameTranscriptProcessor
from transcripts18xx.games import g1830

from tests import context


class TestGameTranscriptProcessor1817(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class TestGameTranscriptProcessor1830(unittest.TestCase):

    @staticmethod
    def _set_not_nan(ser: pd.Series) -> set:
        return set([s for s in ser if pd.notna(s)])

    def _type_int(self, ser: pd.Series) -> bool:
        return any(float(s).is_integer() for s in self._set_not_nan(ser))

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

    def test_columns(self):
        expected = [
            'event', 'phase', 'id', 'line', 'action', 'player', 'amount',
            'private', 'percentage', 'company', 'round', 'source', 'who',
            'location', 'tile', 'rotation', 'direction', 'share_price',
            'train', 'route', 'per_share', 'old_train', 'new_train'
        ]
        self.assertEqual(expected, list(self.df.columns))

    def test_event(self):
        expected = {
            'PrivateAuctioned', 'DoesNotRun', 'TrainRust', 'SelectsHome',
            'OperatesCompany', 'GameOver', 'OperatingRound',
            'PresidentNomination', 'NewPhase', 'CompanyFloats', 'BankBroke',
            'PrivateClosed', 'AllPrivatesClosed', 'PriorityDeal', 'StockRound',
            'SharePriceMoves'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.event))

    def test_phase(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, self._set_not_nan(self.df.phase))

    def test_id(self):
        self.assertEqual(self.df.shape[0], len(self._set_not_nan(self.df.id)))

    def test_action(self):
        expected = {
            'BuyPrivate', 'BuyShare', 'BuyTrain', 'CollectPrivate',
            'ContributeTrain', 'DiscardTrain', 'ExchangeTrain', 'LayTile',
            'ParCompany', 'Pass', 'PassAuction', 'PassPrivate', 'PassTile',
            'PassToken', 'PassTrain', 'PayDivided', 'PlaceBid', 'PlaceToken',
            'ReceiveFunds', 'ReceiveShare', 'RunTrain', 'SellShare',
            'SkipBuyTrain', 'SkipPrivate', 'SkipRunTrain', 'SkipShare',
            'SkipTile', 'SkipToken', 'WithholdDivided'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.action))

    def test_player(self):
        expected = {'mpcoyne', 'riverfiend', 'mpakfm', 'leesin'}
        self.assertEqual(expected, self._set_not_nan(self.df.player))

    def test_amount(self):
        self.assertTrue(self._type_int(self.df.amount))

    def test_private(self):
        expected = {
            'Baltimore & Ohio', 'Champlain & St.Lawrence', 'Mohawk & Hudson',
            'Delaware & Hudson', 'Camden & Amboy', 'Schuylkill Valley'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.private))

    def test_percentage(self):
        self.assertTrue(self._type_int(self.df.percentage))

    def test_company(self):
        expected = {'PRR', 'B&O', 'C&O', 'B&M', 'NYC', 'NYNH', 'ERIE', 'CPR'}
        self.assertEqual(expected, self._set_not_nan(self.df.company))

    def test_round(self):
        expected = {
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
        self.assertEqual(expected, self._set_not_nan(self.df['round']))

    def test_source(self):
        expected = {
            'B&M', 'Baltimore & Ohio', 'Camden & Amboy',
            'Champlain & St.Lawrence', 'Delaware & Hudson', 'ERIE', 'IPO',
            'Mohawk & Hudson', 'NYNH', 'Schuylkill Valley', 'The Depot',
            'market'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.source))

    def test_who(self):
        expected = {
            'B&O', 'leesin', 'riverfiend', 'C&O', 'mpakfm', 'PRR', 'mpcoyne'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.who))

    def test_location(self):
        expected = {
            'A19', 'B10 (Barrie)', 'B12', 'B14', 'B16 (Ottawa)', 'B18',
            'B20 (Burlington)', 'B22', 'C11', 'C13', 'C17', 'C9',
            'D10 (Hamilton & Toronto)', 'D12', 'D16', 'D18', 'D20', 'D8', 'E11',
            'E11 (Dunkirk & Buffalo)', 'E11 (Dunkirk & Buffalo) ', 'E13', 'E19',
            'E19 (Albany)', 'E19 (Albany) ', 'E21', 'E23', 'E23 (Boston)',
            'F10 (Erie)', 'F12', 'F14', 'F16 (Scranton)', 'F16 (Scranton) ',
            'F18', 'F20 (New Haven & Hartford)', 'F22 (Providence)',
            'F22 (Providence) ', 'F6', 'G13', 'G15',
            'G17 (Reading & Allentown)', 'G19', 'G19 (New York & Newark)',
            'G19 (New York & Newark) ', 'G3', 'G5', 'G7 (Akron & Canton)', 'G9',
            'H10 (Pittsburgh)', 'H12', 'H14', 'H16 (Lancaster)',
            'H16 (Lancaster) ', 'H18 (Philadelphia & Trenton)',
            'H18 (Philadelphia & Trenton) ', 'H4 (Columbus)', 'H6', 'H8', 'I15',
            'I15 (Baltimore)', 'I17'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.location))

    def test_tile(self):
        expected = {
            '1', '14', '15', '16', '18', '2', '23', '24', '25', '26', '27',
            '28', '29', '39', '41', '43', '44', '45', '46', '53', '54', '57',
            '58', '59', '61', '62', '63', '65', '66', '67', '69', '7', '70',
            '8', '9'
        }
        self.assertEqual(expected, self._set_not_nan(self.df.tile))

    def test_rotation(self):
        expected = {'0', '1', '2', '3', '4', '5'}
        self.assertEqual(expected, self._set_not_nan(self.df.rotation))

    def test_direction(self):
        expected = {'down', 'right', 'up', 'left'}
        self.assertEqual(expected, self._set_not_nan(self.df.direction))

    def test_share_price(self):
        self.assertTrue(self._type_int(self.df.share_price))

    def test_train(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, self._set_not_nan(self.df.train))

    def test_route(self):
        # Follows: `tile-tile-tile-...` scheme
        pass

    def test_per_share(self):
        self.assertTrue(self._type_int(self.df.per_share))

    def test_old_train(self):
        expected = {'4'}
        self.assertEqual(expected, self._set_not_nan(self.df.old_train))

    def test_new_train(self):
        expected = {'D'}
        self.assertEqual(expected, self._set_not_nan(self.df.new_train))
