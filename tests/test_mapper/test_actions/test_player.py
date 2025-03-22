#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import player


class TestPlayerActions(unittest.TestCase):

    def test_actions(self):
        line = 'riverfiend bids $170 for Camden & Amboy'
        results = player.actions(line)
        self.assertTrue(any(
            result and result.get('action') == 'BidPlaced' for result in
            results)
        )

    def test_bids(self):
        line = 'riverfiend bids $170 for Camden & Amboy'
        expected = {
            'action': 'BidPlaced',
            'player': 'riverfiend',
            'amount': '170',
            'private': 'Camden & Amboy'
        }
        self.assertEqual(expected, player.bids(line))

    def test_operates_company(self):
        line = 'riverfiend bids $170 for Camden & Amboy'
        expected = {
            'action': 'BidPlaced',
            'player': 'riverfiend',
            'amount': '170',
            'private': 'Camden & Amboy'
        }
        self.assertEqual(expected, player.bids(line))

    def test_pars_company(self):
        line = 'leesin pars B&O at $82'
        expected = {
            'action': 'CompanyPared',
            'player': 'leesin',
            'amount': '82',
            'company': 'B&O'
        }
        self.assertEqual(expected, player.pars_company(line))

    def test_declines_sell_shares(self):
        line = 'riverfiend declines to sell shares'
        expected = {
            'action': 'SharesSellSkipped',
            'player': 'riverfiend',
        }
        self.assertEqual(expected, player.declines_sell_shares(line))

    def test_declines_buy_shares(self):
        line = 'riverfiend declines to buy shares'
        expected = {
            'action': 'SharesBuySkipped',
            'player': 'riverfiend',
        }
        self.assertEqual(expected, player.declines_buy_shares(line))

    def test_sells_shares(self):
        line = 'leesin sells 4 shares of B&O and receives $284'
        expected = {
            'action': 'SharesSold',
            'player': 'leesin',
            'percentage': '40',
            'company': 'B&O',
            'amount': '284'
        }
        self.assertEqual(expected, player.sells_shares(line))

    def test_contributes_for_train(self):
        line = 'mpakfm contributes $990'
        expected = {
            'action': 'TrainBuyContributed',
            'player': 'mpakfm',
            'amount': '990'
        }
        self.assertEqual(expected, player.contributes_for_train(line))
