#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from transcripts18xx.pipe import parsing
from transcripts18xx.games import Game1830
from transcripts18xx.engine.states.player import PlayerState
from transcripts18xx.engine.states.company import CompanyState

from tests import context


class TestGameTranscriptProcessor1830(unittest.TestCase):
    df = None

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1830()
        gtp = parsing.GameTranscriptProcessor(Game1830())
        df = gtp.parse_transcript(raw_transcript)
        cls.df = df

    @classmethod
    def tearDownClass(cls) -> None:
        filepath = context.transcript_1830().parent.joinpath(
            context.transcript_1830().stem + '_parsed.csv'
        )
        cls.df.to_csv(filepath, index=False, sep=',')

    def test_shape(self):
        self.assertEqual(1346, self.df.shape[0])
        self.assertEqual(24, self.df.shape[1])

    def test_columns(self):
        expected = [
            'phase', 'type', 'parent', 'id', 'line', 'player', 'amount',
            'private', 'entity', 'source', 'percentage', 'company', 'sequence',
            'location', 'tile', 'rotation', 'direction', 'share_price', 'train',
            'route', 'per_share', 'old_train', 'new_train', 'result'
        ]
        self.assertEqual(sorted(expected), sorted(list(self.df.columns)))

    def test_phase(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, set(self.df.phase.dropna().unique()))

    def test_type(self):
        expected = {
            'AllPrivatesClose', 'BankBroke', 'Bid', 'BuyPrivate', 'BuyShare',
            'BuyTrain', 'Collect', 'CompanyFloats', 'Contribute',
            'DiscardTrain', 'DoesNotRun', 'ExchangeTrain', 'GameOver',
            'LayTile', 'NewPhase', 'OperatesCompany', 'OperatingRound', 'Par',
            'Pass', 'PayOut', 'PlaceToken', 'PresidentNomination',
            'PriorityDeal', 'PrivateAuctioned', 'PrivateCloses', 'ReceiveFunds',
            'ReceiveShare', 'RunTrain', 'SelectsHome', 'SellShares',
            'SharePriceMoves', 'Skip', 'StockRound', 'TrainsRust', 'Withhold'
        }
        self.assertEqual(expected, set(self.df['type'].dropna().unique()))

    def test_parent(self):
        expected = {'Action', 'Event'}
        self.assertEqual(expected, set(self.df.parent.dropna().unique()))

    def test_id(self):
        self.assertEqual(self.df.shape[0], len(self.df.id.dropna().unique()))

    def test_player(self):
        expected = {'mpcoyne', 'riverfiend', 'mpakfm', 'leesin'}
        self.assertEqual(expected, set(self.df.player.dropna().unique()))

    def test_amount(self):
        self.assertTrue(any(
            float(s).is_integer() for s in self.df.amount.dropna().unique())
        )

    def test_private(self):
        expected = {
            'Baltimore & Ohio', 'Champlain & St.Lawrence', 'Mohawk & Hudson',
            'Delaware & Hudson', 'Camden & Amboy', 'Schuylkill Valley'
        }
        self.assertEqual(expected, set(self.df.private.dropna().unique()))

    def test_entity(self):
        expected = {
            'B&M', 'B&O', 'C&O', 'CPR', 'ERIE', 'NYC', 'NYNH', 'PRR', 'leesin',
            'mpakfm', 'mpcoyne', 'riverfiend'
        }
        self.assertEqual(expected, set(self.df.entity.dropna().unique()))

    def test_source(self):
        expected = {
            'Auction', 'B&M', 'Baltimore & Ohio', 'Camden & Amboy',
            'Champlain & St.Lawrence', 'Delaware & Hudson', 'ERIE', 'IPO',
            'Mohawk & Hudson', 'NYNH', 'Schuylkill Valley', 'The Depot',
            'leesin', 'market', 'mpcoyne', 'riverfiend'
        }
        self.assertEqual(expected, set(self.df.source.dropna().unique()))

    def test_percentage(self):
        self.assertTrue(any(
            float(s).is_integer() for s in self.df.percentage.dropna().unique())
        )

    def test_company(self):
        expected = {
            'B&M', 'CPR', 'NYC', 'NYNH', 'ERIE', 'C&O', 'B&O', 'C&O (DH)', 'PRR'
        }
        self.assertEqual(expected, set(self.df.company.dropna().unique()))

    def test_sequence(self):
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
        self.assertEqual(expected, set(self.df.sequence.dropna().unique()))

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
        self.assertEqual(expected, set(self.df.location.dropna().unique()))

    def test_tile(self):
        expected = {
            '1', '14', '15', '16', '18', '2', '23', '24', '25', '26', '27',
            '28', '29', '39', '41', '43', '44', '45', '46', '53', '54', '57',
            '58', '59', '61', '62', '63', '65', '66', '67', '69', '7', '70',
            '8', '9'
        }
        self.assertEqual(expected, set(self.df.tile.dropna().unique()))

    def test_rotation(self):
        expected = {'0', '1', '2', '3', '4', '5'}
        self.assertEqual(expected, set(self.df.rotation.dropna().unique()))

    def test_direction(self):
        expected = {'down', 'right', 'up', 'left'}
        self.assertEqual(expected, set(self.df.direction.dropna().unique()))

    def test_share_price(self):
        self.assertTrue(any(
            float(s).is_integer() for s in
            self.df.share_price.dropna().unique())
        )

    def test_train(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, set(self.df.train.dropna().unique()))

    def test_route(self):
        # Follows: `tile-tile-tile-...` scheme
        pass

    def test_per_share(self):
        self.assertTrue(any(
            float(s).is_integer() for s in self.df.per_share.dropna().unique())
        )

    def test_old_train(self):
        expected = {'4'}
        self.assertEqual(expected, set(self.df.old_train.dropna().unique()))

    def test_new_train(self):
        expected = {'D'}
        self.assertEqual(expected, set(self.df.new_train.dropna().unique()))

    def test_result(self):
        expected = {
            'mpcoyne': 6735, 'leesin': 6648, 'riverfiend': 5523, 'mpakfm': 2740
        }
        self.assertEqual(expected, eval(self.df.iloc[-1, :].result))


class TestTranscriptPostProcessor1830(unittest.TestCase):
    df = None

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1830()
        gtp = parsing.GameTranscriptProcessor(Game1830())
        df = gtp.parse_transcript(raw_transcript)
        tpp = parsing.TranscriptPostProcessor(df, Game1830())
        df = tpp.process()
        cls.df = df

    @classmethod
    def tearDownClass(cls) -> None:
        filepath = context.transcript_1830().parent.joinpath(
            context.transcript_1830().stem + '_processed.csv'
        )
        cls.df.to_csv(filepath, index=False, sep=',')

    def test_shape(self):
        self.assertEqual(1346, self.df.shape[0])
        self.assertEqual(22, self.df.shape[1])

    def test_columns(self):
        expected = [
            'amount', 'company', 'direction', 'id', 'location', 'new_train',
            'old_train', 'parent', 'per_share', 'percentage', 'phase', 'player',
            'private', 'rotation', 'route', 'sequence', 'share_price', 'source',
            'tile', 'train', 'type', 'result'
        ]
        self.assertEqual(sorted(expected), sorted(list(self.df.columns)))

    def test_phase(self):
        expected = {'2', '3', '4', '5', '6', 'D'}
        self.assertEqual(expected, set(self.df.phase.unique()))

    def test_company(self):
        expected = {
            'B&M', 'CPR', 'NYC', 'NYNH', 'ERIE', 'C&O', 'B&O', 'PRR'
        }
        self.assertEqual(expected, set(self.df.company.dropna().unique()))

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
        self.assertEqual(expected, set(self.df.location.dropna().unique()))

    def test_source(self):
        expected = {
            'Auction', 'B&M', 'Baltimore & Ohio', 'Camden & Amboy',
            'Champlain & St.Lawrence', 'Delaware & Hudson', 'ERIE', 'IPO',
            'Mohawk & Hudson', 'NYNH', 'Schuylkill Valley', 'The Depot',
            'market', 'leesin', 'mpcoyne', 'riverfiend'
        }
        self.assertEqual(expected, set(self.df.source.dropna().unique()))

    def test_contributions(self):
        self.assertEqual('CPR', self.df.iloc[933, :].company)
        self.assertEqual('NYC', self.df.iloc[950, :].company)
        self.assertEqual('B&M', self.df.iloc[1089, :].company)


class TestGameStateProcessor1830(unittest.TestCase):
    df = None

    @classmethod
    def setUpClass(cls) -> None:
        raw_transcript = context.transcript_1830()
        gtp = parsing.GameTranscriptProcessor(Game1830())
        parsed = gtp.parse_transcript(raw_transcript)
        tpp = parsing.TranscriptPostProcessor(parsed, Game1830())
        processed = tpp.process()
        gsp = parsing.GameStateProcessor(processed, Game1830())
        df = gsp.generate()
        cls.df = df
        cls.final_state = gsp.final_state()

    @classmethod
    def tearDownClass(cls) -> None:
        filepath = context.transcript_1830().parent.joinpath(
            context.transcript_1830().stem + '_game_state.csv'
        )
        cls.df.to_csv(filepath, index=False, sep=',')

    def isr_1(self):
        return self.df[self.df.sequence == 'ISR 1'].iloc[-1, :]

    def game_over(self):
        return self.df[self.df.sequence == 'OR 8.3'].iloc[-1, :]

    def test_shape(self):
        self.assertEqual(1346, self.df.shape[0])
        self.assertEqual(166, self.df.shape[1])

    def test_final_state(self):
        self.assertIsInstance(self.final_state, dict)
        self.assertEqual(
            ['players', 'companies'], list(self.final_state.keys())
        )
        self.assertEqual(4, len(self.final_state['players']))
        self.assertEqual(8, len(self.final_state['companies']))

    def test_isr_1_mpcoyne(self):
        player = PlayerState('mpcoyne', int(), dict())
        player.cash = 360
        player.value = 780
        player.shares = {
            'B&M': 0, 'B&O': 2, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = False
        player.privates = {'Schuylkill Valley': 20, 'Baltimore & Ohio': 220}
        expected = player.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_riverfiend(self):
        player = PlayerState('riverfiend', int(), dict())
        player.cash = 525
        player.value = 595
        player.shares = {
            'B&M': 0, 'B&O': 0, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = True
        player.privates = {'Delaware & Hudson': 70}
        expected = player.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_leesin(self):
        player = PlayerState('leesin', int(), dict())
        player.cash = 250
        player.value = 520
        player.shares = {
            'B&M': 0, 'B&O': 0, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 1
        }
        player.priority_deal = False
        player.privates = {'Mohawk & Hudson': 110, 'Camden & Amboy': 160}
        expected = player.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_mpakfm(self):
        player = PlayerState('mpakfm', int(), dict())
        player.cash = 560
        player.value = 600
        player.shares = {
            'B&M': 0, 'B&O': 0, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = False
        player.privates = {'Champlain & St.Lawrence': 40}
        expected = player.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_Boston_and_Maine_Railroad(self):
        company = CompanyState('B&M', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_Baltimore_and_Ohio(self):
        company = CompanyState('B&O', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 8
        company.market = 0
        company.president = 'mpcoyne'
        company.share_price = 90
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_Chesapeake_and_Ohio_Railroad(self):
        company = CompanyState('C&O', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_Canadian_Pacific_Railroad(self):
        company = CompanyState('CPR', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_Erie_Railroad(self):
        company = CompanyState('ERIE', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_New_York_Central_Railroad(self):
        company = CompanyState('NYC', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_New_York_New_Haven_and_Hartford_Railroad(self):
        company = CompanyState('NYNH', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_isr_1_Pennsylvania_Railroad(self):
        company = CompanyState('PRR', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 9
        company.market = 0
        company.president = None
        company.share_price = 0
        expected = company.flatten().to_dict()
        result = self.isr_1().loc[
            [col for col in self.isr_1().index if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_mpcoyne(self):
        player = PlayerState('mpcoyne', int(), dict())
        player.cash = 3304
        player.value = 6735
        player.shares = {
            'B&M': 6, 'B&O': 6, 'C&O': 1, 'CPR': 0,
            'ERIE': 4, 'NYC': 1, 'NYNH': 0, 'PRR': 1
        }
        player.priority_deal = False
        player.privates = dict()
        expected = player.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_riverfiend(self):
        player = PlayerState('riverfiend', int(), dict())
        player.cash = 3560
        player.value = 5523
        player.shares = {
            'B&M': 3, 'B&O': 0, 'C&O': 6, 'CPR': 0,
            'ERIE': 6, 'NYC': 1, 'NYNH': 2, 'PRR': 1
        }
        player.priority_deal = False
        player.privates = dict()
        expected = player.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_leesin(self):
        player = PlayerState('leesin', int(), dict())
        player.cash = 3432
        player.value = 6648
        player.shares = {
            'B&M': 1, 'B&O': 2, 'C&O': 1, 'CPR': 6,
            'ERIE': 0, 'NYC': 2, 'NYNH': 6, 'PRR': 8
        }
        player.priority_deal = False
        player.privates = dict()
        expected = player.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_mpakfm(self):
        player = PlayerState('mpakfm', int(), dict())
        player.cash = 1260
        player.value = 2740
        player.shares = {
            'B&M': 0, 'B&O': 2, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 6, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = True
        player.privates = dict()
        expected = player.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(player.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_Boston_and_Maine_Railroad(self):
        company = CompanyState('B&M', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 0
        company.market = 0
        company.president = 'mpcoyne'
        company.share_price = 100
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_Baltimore_and_Ohio(self):
        company = CompanyState('B&O', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 1, '6': 1, 'D': 0}
        company.ipo = 0
        company.market = 0
        company.president = 'mpcoyne'
        company.share_price = 350
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_Chesapeake_and_Ohio_Railroad(self):
        company = CompanyState('C&O', dict())
        company.cash = 140
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 1, '6': 0, 'D': 0}
        company.ipo = 0
        company.market = 2
        company.president = 'riverfiend'
        company.share_price = 90
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_Canadian_Pacific_Railroad(self):
        company = CompanyState('CPR', dict())
        company.cash = 40
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 3
        company.market = 1
        company.president = 'leesin'
        company.share_price = 125
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_Erie_Railroad(self):
        company = CompanyState('ERIE', dict())
        company.cash = 2
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 1, 'D': 0}
        company.ipo = 0
        company.market = 0
        company.president = 'riverfiend'
        company.share_price = 111
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_New_York_Central_Railroad(self):
        company = CompanyState('NYC', dict())
        company.cash = 56
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 0
        company.market = 0
        company.president = 'mpakfm'
        company.share_price = 130
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_New_York_New_Haven_and_Hartford_Railroad(self):
        company = CompanyState('NYNH', dict())
        company.cash = 170
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 1, '6': 0, 'D': 0}
        company.ipo = 0
        company.market = 2
        company.president = 'leesin'
        company.share_price = 130
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)

    def test_game_over_Pennsylvania_Railroad(self):
        company = CompanyState('PRR', dict())
        company.cash = 40
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 0
        company.market = 0
        company.president = 'leesin'
        company.share_price = 67
        expected = company.flatten().to_dict()
        result = self.game_over().loc[
            [col for col in self.game_over().index
             if col.startswith(company.name)]
        ].to_dict()
        self.assertEqual(expected, result)
