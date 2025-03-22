#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import common


class TestCommonActions(unittest.TestCase):

    def test_actions(self):
        line = 'mpcoyne buys Schuylkill Valley for $20'
        results = common.actions(line)
        self.assertTrue(any(
            result and result.get('action') == 'PrivateBought' for result in
            results)
        )

    def test_receives_share(self):
        line = 'leesin receives a 10% share of PRR'
        expected = {
            'action': 'ShareReceived',
            'player': 'leesin',
            'percentage': '10',
            'company': 'PRR'
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
        line = 'riverfiend buys a 20% share of ERIE from the IPO for $200'
        expected = {
            'action': 'ShareBought',
            'player': 'riverfiend',
            'percentage': '20',
            'company': 'ERIE',
            'source': 'IPO',
            'amount': '200'
        }
        self.assertEqual(expected, common.buys(line))

    def test_buys_train(self):
        line = 'PRR buys a 3 train for $180 from The Depot'
        expected = {
            'action': 'TrainBought',
            'company': 'PRR',
            'train': '3',
            'amount': '180',
            'source': 'The Depot'
        }
        self.assertEqual(expected, common.buys(line))

    def test_buys_private(self):
        line = 'mpcoyne buys Schuylkill Valley for $20'
        expected = {
            'action': 'PrivateBought',
            'player': 'mpcoyne',
            'private': 'Schuylkill Valley',
            'amount': '20'
        }
        self.assertEqual(expected, common.buys(line))

    def test_collects(self):
        line = 'mpakfm collects $10 from Champlain & St.Lawrence'
        expected = {
            'action': 'Collect',
            'who': 'mpakfm',
            'amount': '10',
            'source': 'Champlain & St.Lawrence'
        }
        self.assertEqual(expected, common.collects(line))

    def test_passes(self):
        line = 'riverfiend passes'
        expected = {
            'action': 'Passed',
            'who': 'riverfiend'
        }
        self.assertEqual(expected, common.passes(line))
