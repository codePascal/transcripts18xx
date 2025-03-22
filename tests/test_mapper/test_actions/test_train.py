#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import train


class TestTrainActions(unittest.TestCase):

    def test_run_train(self):
        line = 'B&O runs a 3 train for $90: I15-H12-H10'
        expected = {
            'action': 'TrainRan',
            'company': 'B&O',
            'train': '3',
            'amount': '90',
            'route': 'I15-H12-H10'
        }
        self.assertEqual(expected, train.run_train(line))

        line = 'B&O runs a D train for $90: I15-H12-H10'
        expected = {
            'action': 'TrainRan',
            'company': 'B&O',
            'train': 'D',
            'amount': '90',
            'route': 'I15-H12-H10'
        }
        self.assertEqual(expected, train.run_train(line))

    def test_buy_train(self):
        line = 'B&O buys a 3 train for $180 from The Depot'
        expected = {
            'action': 'TrainBought',
            'company': 'B&O',
            'train': '3',
            'amount': '180',
            'source': 'The Depot'
        }
        self.assertEqual(expected, train.buy_train(line))

    def test_pass_train(self):
        line = 'B&O passes buy trains'
        expected = {
            'action': 'TrainPassed',
            'company': 'B&O'
        }
        self.assertEqual(expected, train.pass_train(line))

    def test_skip_run_train(self):
        line = 'B&O skips run routes'
        expected = {
            'action': 'TrainRunSkipped',
            'company': 'B&O',
        }
        self.assertEqual(expected, train.skip_run_train(line))

    def test_skip_buy_train(self):
        line = 'B&O skips buy trains'
        expected = {
            'action': 'TrainBuySkipped',
            'company': 'B&O',
        }
        self.assertEqual(expected, train.skip_buy_train(line))

    def test_discard_train(self):
        line = 'B&O discards 3'
        expected = {
            'action': 'TrainDiscarded',
            'company': 'B&O',
            'train': '3'
        }
        self.assertEqual(expected, train.discard_train(line))

    def test_exchange_train(self):
        line = 'B&O exchanges a 4 for a D train for $800 from The Depot'
        expected = {
            'action': 'TrainExchanged',
            'company': 'B&O',
            'old_train': '4',
            'new_train': 'D',
            'amount': '800',
            'source': 'The Depot'
        }
        self.assertEqual(expected, train.exchange_train(line))

    def test_contribute_for_train(self):
        line = 'player1 contributes $990'
        expected = {
            'action': 'TrainBuyContributed',
            'player': 'player1',
            'amount': '990'
        }
        self.assertEqual(expected, train.contribute_for_train(line))
