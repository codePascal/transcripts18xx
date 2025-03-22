#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import player


class TestPlayerActions(unittest.TestCase):

    def test_bids(self):
        line = 'player1 bids $170 for Camden & Amboy'
        expected = {
            'action': 'BidPlaced',
            'player': 'player1',
            'amount': '170',
            'private': 'Camden & Amboy'
        }
        self.assertEqual(expected, player.bids(line))

    def test_pars_company(self):
        line = 'player1 pars B&O at $82'
        expected = {
            'action': 'CompanyPared',
            'player': 'player1',
            'amount': '82',
            'company': 'B&O'
        }
        self.assertEqual(expected, player.pars_company(line))

    def test_declines_sell_shares(self):
        line = 'player1 declines to sell shares'
        expected = {
            'action': 'SharesSellSkipped',
            'player': 'player1',
        }
        self.assertEqual(expected, player.declines_sell_shares(line))

    def test_declines_buy_shares(self):
        line = 'player1 declines to buy shares'
        expected = {
            'action': 'SharesBuySkipped',
            'player': 'player1',
        }
        self.assertEqual(expected, player.declines_buy_shares(line))

    def test_sells_shares(self):
        line = 'player1 sells 4 shares of B&O and receives $284'
        expected = {
            'action': 'SharesSold',
            'player': 'player1',
            'percentage': '40',
            'company': 'B&O',
            'amount': '284'
        }
        self.assertEqual(expected, player.sells_shares(line))

    def test_contributes_for_train(self):
        line = 'player1 contributes $990'
        expected = {
            'action': 'TrainBuyContributed',
            'player': 'player1',
            'amount': '990'
        }
        self.assertEqual(expected, player.contributes_for_train(line))
