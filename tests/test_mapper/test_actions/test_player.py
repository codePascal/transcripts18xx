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
        # TODO
        pass

    def test_pars_company(self):
        line = 'leesin pars NYNH at $82'
        # TODO

    def test_declines_sell_shares(self):
        line = 'riverfiend declines to sell shares'
        # TODO

    def test_declines_buy_shares(self):
        # TODO
        pass

    def test_sells_shares(self):
        line = 'leesin sells 4 shares of PRR and receives $284'
        # TODO

    def test_contributes_for_train(self):
        line = 'mpakfm contributes $990'
        expected = {
            'action': 'TrainBuyContributed',
            'player': 'mpakfm',
            'amount': '990'
        }
        self.assertEqual(expected, player.contributes_for_train(line))
