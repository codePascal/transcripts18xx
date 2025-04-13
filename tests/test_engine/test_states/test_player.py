#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.engine.states import player


class TestPlayerState(unittest.TestCase):

    def setUp(self) -> None:
        self.player = player.PlayerState(
            'player1', 100, dict(company1=0, company2=0)
        )

    def test_repr(self):
        self.assertEqual(
            str(
                "PlayerState(name='player1', cash=100, privates={}, value=100, "
                "shares={'company1': 0, 'company2': 0}, priority_deal=False)"
            ),
            self.player.__repr__()
        )

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
        self.player.sells_private('private1', 150)
        self.assertEqual(dict(), self.player.privates)
        self.assertEqual(250, self.player.cash)

    def test_contributes(self):
        self.player.contributes(200)
        self.assertEqual(-100, self.player.cash)

    def test_receives_share(self):
        self.player.receives_share('company1', 2)
        self.assertEqual(2, self.player.shares['company1'])

    def test_has_priority_deal(self):
        self.player.has_priority_deal()
        self.assertTrue(self.player.priority_deal)


class TestPlayers(unittest.TestCase):

    def setUp(self) -> None:
        self.players = player.Players(
            ['player1', 'player2', 'player3'], ['company1', 'company2'], 450
        )

    def test_repr(self):
        self.assertEqual(
            str(
                "PlayerState(name='player1', cash=150, privates={}, value=150, "
                "shares={'company1': 0, 'company2': 0}, priority_deal=False)\n"
                "PlayerState(name='player2', cash=150, privates={}, value=150, "
                "shares={'company1': 0, 'company2': 0}, priority_deal=False)\n"
                "PlayerState(name='player3', cash=150, privates={}, value=150, "
                "shares={'company1': 0, 'company2': 0}, priority_deal=False)\n"
            ),
            self.players.__repr__()
        )
