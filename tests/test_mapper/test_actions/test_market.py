#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import market


class TestMarketActions(unittest.TestCase):

    def test_receive_share(self):
        line = 'player1 receives a 10% share of B&O'
        expected = {
            'action': 'ShareReceived',
            'player': 'player1',
            'percentage': '10',
            'company': 'B&O'
        }
        self.assertEqual(expected, market.receive_share(line))

    def test_receive_funds(self):
        line = 'C&O receives $670'
        expected = {
            'action': 'FundsReceived',
            'company': 'C&O',
            'amount': '670'
        }
        self.assertEqual(expected, market.receive_funds(line))

    def test_buy_share(self):
        line = 'player1 buys a 20% share of ERIE from the IPO for $200'
        expected = {
            'action': 'ShareBought',
            'player': 'player1',
            'percentage': '20',
            'company': 'ERIE',
            'source': 'IPO',
            'amount': '200'
        }
        self.assertEqual(expected, market.buy_share(line))

    def test_decline_sell_share(self):
        line = 'player1 declines to sell shares'
        expected = {
            'action': 'ShareSellSkipped',
            'player': 'player1',
        }
        self.assertEqual(expected, market.decline_sell_shares(line))

    def test_decline_buy_share(self):
        line = 'player1 declines to buy shares'
        expected = {
            'action': 'ShareBuySkipped',
            'player': 'player1',
        }
        self.assertEqual(expected, market.decline_buy_shares(line))

    def test_sell_share(self):
        line = 'player1 sells 4 shares of B&O and receives $284'
        expected = {
            'action': 'ShareSold',
            'player': 'player1',
            'percentage': '40',
            'company': 'B&O',
            'amount': '284'
        }
        self.assertEqual(expected, market.sell_share(line))

    def test_bid(self):
        line = 'player1 bids $170 for Camden & Amboy'
        expected = {
            'action': 'BidPlaced',
            'player': 'player1',
            'amount': '170',
            'private': 'Camden & Amboy'
        }
        self.assertEqual(expected, market.bid(line))

    def test_par_company(self):
        line = 'player1 pars B&O at $82'
        expected = {
            'action': 'CompanyPared',
            'player': 'player1',
            'amount': '82',
            'company': 'B&O'
        }
        self.assertEqual(expected, market.par_company(line))
