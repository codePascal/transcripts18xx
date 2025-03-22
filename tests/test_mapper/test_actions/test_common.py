#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import common


class TestCommonActions(unittest.TestCase):

    def test_receives_share(self):
        line = 'player1 receives a 10% share of B&O'
        expected = {
            'action': 'ShareReceived',
            'player': 'player1',
            'percentage': '10',
            'company': 'B&O'
        }
        self.assertEqual(expected, common.receives(line))

    def test_receives_funds(self):
        line = 'C&O receives $670'
        expected = {
            'action': 'FundsReceived',
            'company': 'C&O',
            'amount': '670'
        }
        self.assertEqual(expected, common.receives(line))

    def test_buys_share(self):
        line = 'player1 buys a 20% share of ERIE from the IPO for $200'
        expected = {
            'action': 'ShareBought',
            'player': 'player1',
            'percentage': '20',
            'company': 'ERIE',
            'source': 'IPO',
            'amount': '200'
        }
        self.assertEqual(expected, common.buys(line))

    def test_buys_train(self):
        line = 'B&O buys a 3 train for $180 from The Depot'
        expected = {
            'action': 'TrainBought',
            'company': 'B&O',
            'train': '3',
            'amount': '180',
            'source': 'The Depot'
        }
        self.assertEqual(expected, common.buys(line))

    def test_buys_private_from_auction(self):
        line = 'player1 buys Schuylkill Valley for $20'
        expected = {
            'action': 'PrivateBought',
            'player': 'player1',
            'private': 'Schuylkill Valley',
            'amount': '20'
        }
        self.assertEqual(expected, common.buys(line))

        line = 'player1 wins the auction for Schuylkill Valley with a bid of $30'
        expected = {
            'action': 'PrivateBought',
            'player': 'player1',
            'private': 'Schuylkill Valley',
            'amount': '30'
        }
        self.assertEqual(expected, common.buys(line))

        line = 'player1 wins the auction for Schuylkill Valley with the only bid of $40'
        expected = {
            'action': 'PrivateBought',
            'player': 'player1',
            'private': 'Schuylkill Valley',
            'amount': '40'
        }
        self.assertEqual(expected, common.buys(line))

    def test_buys_private_from_player(self):
        line = 'B&O buys Schuylkill Valley from player1 for $120'
        expected = {
            'action': 'PrivateBought',
            'player': 'player1',
            'company': 'B&O',
            'private': 'Schuylkill Valley',
            'amount': '120'
        }
        self.assertEqual(expected, common.buys(line))

    def test_collects(self):
        line = 'player1 collects $10 from Champlain & St.Lawrence'
        expected = {
            'action': 'Collect',
            'who': 'player1',
            'amount': '10',
            'source': 'Champlain & St.Lawrence'
        }
        self.assertEqual(expected, common.collects(line))

    def test_passes(self):
        line = 'player1 passes'
        expected = {
            'action': 'Passed',
            'player': 'player1'
        }
        self.assertEqual(expected, common.passes(line))

    def test_passes_no_valid_actions(self):
        line = 'player1 has no valid actions and passes'
        expected = {
            'action': 'Passed',
            'player': 'player1'
        }
        self.assertEqual(expected, common.passes(line))

    def test_passes_auction(self):
        line = 'player1 passes on Mohawk & Hudson'
        expected = {
            'action': 'AuctionPassed',
            'player': 'player1',
            'private': 'Mohawk & Hudson'
        }
        self.assertEqual(expected, common.passes(line))

    def test_passes_privates(self):
        line = 'B&O passes buy companies'
        expected = {
            'action': 'PrivatesPassed',
            'company': 'B&O'
        }
        self.assertEqual(expected, common.passes(line))

    def test_passes_trains(self):
        line = 'B&O passes buy trains'
        expected = {
            'action': 'TrainsPassed',
            'company': 'B&O'
        }
        self.assertEqual(expected, common.passes(line))

    def test_passes_tiles(self):
        line = 'B&O passes lay/upgrade track'
        expected = {
            'action': 'TilesPassed',
            'company': 'B&O'
        }
        self.assertEqual(expected, common.passes(line))

    def test_passes_token(self):
        line = 'B&O passes place a token'
        expected = {
            'action': 'TokenPassed',
            'company': 'B&O'
        }
        self.assertEqual(expected, common.passes(line))

