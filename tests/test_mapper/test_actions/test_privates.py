#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import privates


class TestPrivateActions(unittest.TestCase):

    def test_buy_private(self):
        line = 'player1 buys Schuylkill Valley for $20'
        expected = {
            'action': privates.PrivatesActions.BuyPrivate.name,
            'player': 'player1',
            'private': 'Schuylkill Valley',
            'amount': '20'
        }
        self.assertEqual(expected, privates.buy_private(line))

        line = str(
            'player1 wins the auction for Schuylkill Valley with a bid of $30'
        )
        expected = {
            'action': privates.PrivatesActions.BuyPrivate.name,
            'player': 'player1',
            'private': 'Schuylkill Valley',
            'amount': '30'
        }
        self.assertEqual(expected, privates.buy_private(line))

        line = str(
            'player1 wins the auction for Schuylkill Valley with the only bid '
            'of $40'
        )
        expected = {
            'action': privates.PrivatesActions.BuyPrivate.name,
            'player': 'player1',
            'private': 'Schuylkill Valley',
            'amount': '40'
        }
        self.assertEqual(expected, privates.buy_private(line))

        line = 'B&O buys Schuylkill Valley from player1 for $120'
        expected = {
            'action': privates.PrivatesActions.BuyPrivate.name,
            'player': 'player1',
            'company': 'B&O',
            'private': 'Schuylkill Valley',
            'amount': '120'
        }
        self.assertEqual(expected, privates.buy_private(line))

    def test_skip_private(self):
        line = 'B&O skips buy companies'
        expected = {
            'action': privates.PrivatesActions.SkipPrivate.name,
            'company': 'B&O'
        }
        self.assertEqual(expected, privates.skip_private(line))

    def test_pass_private(self):
        line = 'B&O passes buy companies'
        expected = {
            'action': privates.PrivatesActions.PassPrivate.name,
            'company': 'B&O'
        }
        self.assertEqual(expected, privates.pass_private(line))

    def test_pass_auction(self):
        line = 'player1 passes on Mohawk & Hudson'
        expected = {
            'action': privates.PrivatesActions.PassAuction.name,
            'player': 'player1',
            'private': 'Mohawk & Hudson'
        }
        self.assertEqual(expected, privates.pass_auction(line))

    def test_collect_from_private(self):
        line = 'player1 collects $10 from Champlain & St.Lawrence'
        expected = {
            'action': privates.PrivatesActions.CollectPrivate.name,
            'who': 'player1',
            'amount': '10',
            'source': 'Champlain & St.Lawrence'
        }
        self.assertEqual(expected, privates.collect_from_private(line))
