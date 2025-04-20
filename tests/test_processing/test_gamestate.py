#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from transcripts18xx.processing.gamestate import GameStateProcessor
from transcripts18xx.games import Game1830
from transcripts18xx.engine.states.player import PlayerState
from transcripts18xx.engine.states.company import CompanyState

from tests import context


class TestGameStateProcessor1830(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        df = pd.read_csv(context.processed_transcript_1830())
        gsp = GameStateProcessor(df, Game1830())
        gsp.generate()
        cls.df = gsp.save_to_dataframe(context.transcript_1830())

    def isr_1(self):
        return self.df[self.df.sequence == 'ISR 1'].iloc[-1, :]

    def game_over(self):
        return self.df[self.df.sequence == 'OR 8.3'].iloc[-1, :]

    def test_isr_1_player1(self):
        player = PlayerState('player1', int(), dict())
        player.cash = 360
        player.value = 780
        player.shares = {
            'B&M': 0, 'B&O': 2, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = False
        player.privates = {'Schuylkill Valley': 20, 'Baltimore & Ohio': 220}
        self.assertEqual(player, PlayerState.eval(self.isr_1().player1))

    def test_isr_1_player2(self):
        player = PlayerState('player2', int(), dict())
        player.cash = 525
        player.value = 595
        player.shares = {
            'B&M': 0, 'B&O': 0, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = True
        player.privates = {'Delaware & Hudson': 70}
        self.assertEqual(player, PlayerState.eval(self.isr_1().player2))

    def test_isr_1_player3(self):
        player = PlayerState('player3', int(), dict())
        player.cash = 250
        player.value = 520
        player.shares = {
            'B&M': 0, 'B&O': 0, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 1
        }
        player.priority_deal = False
        player.privates = {'Mohawk & Hudson': 110, 'Camden & Amboy': 160}
        self.assertEqual(player, PlayerState.eval(self.isr_1().player3))

    def test_isr_1_player4(self):
        player = PlayerState('player4', int(), dict())
        player.cash = 560
        player.value = 600
        player.shares = {
            'B&M': 0, 'B&O': 0, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 0, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = False
        player.privates = {'Champlain & St.Lawrence': 40}
        self.assertEqual(player, PlayerState.eval(self.isr_1().player4))

    def test_isr_1_Boston_and_Maine_Railroad(self):
        company = CompanyState('B&M', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        self.assertEqual(company, CompanyState.eval(self.isr_1()['B&M']))

    def test_isr_1_Baltimore_and_Ohio(self):
        company = CompanyState('B&O', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 8
        company.market = 0
        company.president = 'player1'
        company.share_price = 90
        self.assertEqual(company, CompanyState.eval(self.isr_1()['B&O']))

    def test_isr_1_Chesapeake_and_Ohio_Railroad(self):
        company = CompanyState('C&O', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        self.assertEqual(company, CompanyState.eval(self.isr_1()['C&O']))

    def test_isr_1_Canadian_Pacific_Railroad(self):
        company = CompanyState('CPR', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        self.assertEqual(company, CompanyState.eval(self.isr_1()['CPR']))

    def test_isr_1_Erie_Railroad(self):
        company = CompanyState('ERIE', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        self.assertEqual(company, CompanyState.eval(self.isr_1()['ERIE']))

    def test_isr_1_New_York_Central_Railroad(self):
        company = CompanyState('NYC', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        self.assertEqual(company, CompanyState.eval(self.isr_1()['NYC']))

    def test_isr_1_New_York_New_Haven_and_Hartford_Railroad(self):
        company = CompanyState('NYNH', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 10
        company.market = 0
        company.president = None
        company.share_price = 0
        self.assertEqual(company, CompanyState.eval(self.isr_1()['NYNH']))

    def test_isr_1_Pennsylvania_Railroad(self):
        company = CompanyState('PRR', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}
        company.ipo = 9
        company.market = 0
        company.president = None
        company.share_price = 0
        self.assertEqual(company, CompanyState.eval(self.isr_1()['PRR']))

    def test_game_over_player1(self):
        player = PlayerState('player1', int(), dict())
        player.cash = 3304
        player.value = 6735
        player.shares = {
            'B&M': 6, 'B&O': 6, 'C&O': 1, 'CPR': 0,
            'ERIE': 4, 'NYC': 1, 'NYNH': 0, 'PRR': 1
        }
        player.priority_deal = False
        player.privates = dict()
        self.assertEqual(player, PlayerState.eval(self.game_over().player1))

    def test_game_over_player2(self):
        player = PlayerState('player2', int(), dict())
        player.cash = 3560
        player.value = 5523
        player.shares = {
            'B&M': 3, 'B&O': 0, 'C&O': 6, 'CPR': 0,
            'ERIE': 6, 'NYC': 1, 'NYNH': 2, 'PRR': 1
        }
        player.priority_deal = False
        player.privates = dict()
        self.assertEqual(player, PlayerState.eval(self.game_over().player2))

    def test_game_over_player3(self):
        player = PlayerState('player3', int(), dict())
        player.cash = 3432
        player.value = 6648
        player.shares = {
            'B&M': 1, 'B&O': 2, 'C&O': 1, 'CPR': 6,
            'ERIE': 0, 'NYC': 2, 'NYNH': 6, 'PRR': 8
        }
        player.priority_deal = False
        player.privates = dict()
        self.assertEqual(player, PlayerState.eval(self.game_over().player3))

    def test_game_over_player4(self):
        player = PlayerState('player4', int(), dict())
        player.cash = 1260
        player.value = 2740
        player.shares = {
            'B&M': 0, 'B&O': 2, 'C&O': 0, 'CPR': 0,
            'ERIE': 0, 'NYC': 6, 'NYNH': 0, 'PRR': 0
        }
        player.priority_deal = True
        player.privates = dict()
        self.assertEqual(player, PlayerState.eval(self.game_over().player4))

    def test_game_over_Boston_and_Maine_Railroad(self):
        company = CompanyState('B&M', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 0
        company.market = 0
        company.president = 'player1'
        company.share_price = 100
        self.assertEqual(company, CompanyState.eval(self.game_over()['B&M']))

    def test_game_over_Baltimore_and_Ohio(self):
        company = CompanyState('B&O', dict())
        company.cash = 0
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 1, '6': 1, 'D': 0}
        company.ipo = 0
        company.market = 0
        company.president = 'player1'
        company.share_price = 350
        self.assertEqual(company, CompanyState.eval(self.game_over()['B&O']))

    def test_game_over_Chesapeake_and_Ohio_Railroad(self):
        company = CompanyState('C&O', dict())
        company.cash = 140
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 1, '6': 0, 'D': 0}
        company.ipo = 0
        company.market = 2
        company.president = 'player2'
        company.share_price = 90
        self.assertEqual(company, CompanyState.eval(self.game_over()['C&O']))

    def test_game_over_Canadian_Pacific_Railroad(self):
        company = CompanyState('CPR', dict())
        company.cash = 40
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 3
        company.market = 1
        company.president = 'player3'
        company.share_price = 125
        self.assertEqual(company, CompanyState.eval(self.game_over()['CPR']))

    def test_game_over_Erie_Railroad(self):
        company = CompanyState('ERIE', dict())
        company.cash = 2
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 1, 'D': 0}
        company.ipo = 0
        company.market = 0
        company.president = 'player2'
        company.share_price = 111
        self.assertEqual(company, CompanyState.eval(self.game_over()['ERIE']))

    def test_game_over_New_York_Central_Railroad(self):
        company = CompanyState('NYC', dict())
        company.cash = 56
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 0
        company.market = 0
        company.president = 'player4'
        company.share_price = 130
        self.assertEqual(company, CompanyState.eval(self.game_over()['NYC']))

    def test_game_over_New_York_New_Haven_and_Hartford_Railroad(self):
        company = CompanyState('NYNH', dict())
        company.cash = 170
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 1, '6': 0, 'D': 0}
        company.ipo = 0
        company.market = 2
        company.president = 'player3'
        company.share_price = 130
        self.assertEqual(company, CompanyState.eval(self.game_over()['NYNH']))

    def test_game_over_Pennsylvania_Railroad(self):
        company = CompanyState('PRR', dict())
        company.cash = 40
        company.privates = dict()
        company.trains = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 1}
        company.ipo = 0
        company.market = 0
        company.president = 'player3'
        company.share_price = 67
        self.assertEqual(company, CompanyState.eval(self.game_over()['PRR']))
