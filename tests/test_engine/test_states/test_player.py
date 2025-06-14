#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from transcripts18xx.engine.states import player


class TestPlayerState(unittest.TestCase):

    def setUp(self) -> None:
        self.player = player.PlayerState(
            'player1', 100, dict(company1=0, company2=0)
        )

    def test_repr(self):
        self.assertEqual(
            str(
                "{'name': 'player1', 'cash': 100, 'privates': {}, "
                "'value': 100, 'shares': {'company1': 0, 'company2': 0}, "
                "'priority_deal': False}"
            ),
            self.player.__repr__()
        )

    def test_eval(self):
        rep = str(
            "{'name': 'player1', 'cash': 150, 'privates': {}, "
            "'value': 200, 'shares': {'company1': 2, 'company2': 0}, "
            "'priority_deal': True}"
        )
        st = player.PlayerState.eval(rep)
        self.assertEqual('player1', st.name)
        self.assertEqual(150, st.cash)
        self.assertEqual(dict(), st.privates)
        self.assertEqual(200, st.value)
        self.assertEqual(dict(company1=2, company2=0), st.shares)
        self.assertTrue(st.priority_deal)

    def test_flatten(self):
        flatten = self.player.flatten()
        self.assertIsInstance(flatten, pd.Series)
        self.assertEqual(100, flatten['player1_cash'])
        self.assertEqual('{}', flatten['player1_privates'])
        self.assertEqual(100, flatten['player1_value'])
        self.assertEqual(0, flatten['player1_shares_company1'])
        self.assertEqual(0, flatten['player1_shares_company2'])
        self.assertFalse(flatten['player1_priority_deal'])

    def test_update(self):
        self.player.shares['company1'] = 2
        self.player.shares['company2'] = 1
        self.player.privates['private1'] = 100
        self.player.update(dict(company1=50, company2=40))
        self.assertEqual(340, self.player.value)

    def test_receives_dividend(self):
        self.player.shares['company1'] = 2
        self.player.receives_dividend('company1', 10)
        self.assertEqual(120, self.player.cash)

    def test_buys_shares(self):
        self.player.buys_shares('company1', 2, 45)
        self.assertEqual(55, self.player.cash)
        self.assertEqual(2, self.player.shares['company1'])

    def test_sells_shares(self):
        self.player.sells_shares('company1', 1, 90)
        self.assertEqual(190, self.player.cash)
        self.assertEqual(-1, self.player.shares['company1'])

    def test_sells_private(self):
        self.player.privates['private1'] = 200
        self.player.sells_private('private1', 150, 60)
        self.assertEqual(dict(), self.player.privates)
        self.assertEqual(250, self.player.cash)

    def test_contributes(self):
        self.player.contributes(200)
        self.assertEqual(-100, self.player.cash)

    def test_receives_share(self):
        self.player.receives_share('company1', 2)
        self.assertEqual(2, self.player.shares['company1'])

    def test_has_priority_deal(self):
        self.player.has_priority_deal(True)
        self.assertTrue(self.player.priority_deal)

        self.player.has_priority_deal(False)
        self.assertFalse(self.player.priority_deal)

    def test_goes_bankrupt(self):
        self.player.cash = 100
        self.player.goes_bankrupt()
        self.assertEqual(0, self.player.cash)

    def test_exchanges_private_for_share(self):
        self.player.privates['private1'] = 20
        self.player.exchanges_private_for_share('private1', 2, 'company2')
        self.assertFalse(self.player.privates)
        self.assertEqual(2, self.player.shares['company2'])


class TestPlayers(unittest.TestCase):

    def setUp(self) -> None:
        self.players = player.Players(
            ['player1', 'player2', 'player3'], ['company1', 'company2'], 450
        )

    def test_repr(self):
        self.assertEqual(
            str(
                "{'name': 'player1', 'cash': 150, 'privates': {}, "
                "'value': 150, 'shares': {'company1': 0, 'company2': 0}, "
                "'priority_deal': False}\n"
                "{'name': 'player2', 'cash': 150, 'privates': {}, "
                "'value': 150, 'shares': {'company1': 0, 'company2': 0}, "
                "'priority_deal': False}\n"
                "{'name': 'player3', 'cash': 150, 'privates': {}, "
                "'value': 150, 'shares': {'company1': 0, 'company2': 0}, "
                "'priority_deal': False}\n"
            ),
            self.players.__repr__()
        )

    def test_update(self):
        share_prices = dict(share_prices=(dict(company1=50, company2=40)))
        self.players.states[0].shares = dict(company1=2, company2=1)
        self.players.states[1].shares = dict(company1=1, company2=0)
        self.players.states[2].shares = dict(company1=0, company2=3)
        self.players.update(share_prices)
        self.assertEqual(290, self.players.states[0].value)
        self.assertEqual(200, self.players.states[1].value)
        self.assertEqual(270, self.players.states[2].value)
