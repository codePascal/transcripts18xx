#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import company


class TestCompanyActions(unittest.TestCase):

    def test_actions(self):
        line = 'B&O runs a 2 train for $70: F6-F2'
        results = company.actions(line)
        self.assertTrue(any(
            result and result.get('action') == 'TrainRan' for result in
            results)
        )

    def test_places_token(self):
        line = 'B&O places a token on F16 (Scranton)'
        expected = {
            'action': 'TokenPlaced',
            'company': 'B&O',
            'location': 'F16 (Scranton)'
        }
        self.assertEqual(expected, company.places_token(line))

    def test_lays_tile(self):
        line = 'B&O lays tile #7 with rotation 1 on I17'
        expected = {
            'action': 'TilePlaced',
            'company': 'B&O',
            'tile': '7',
            'rotation': '1',
            'location': 'I17'
        }
        self.assertEqual(expected, company.lays_tile(line))

    def test_runs_train(self):
        line = 'B&O runs a 3 train for $90: I15-H12-H10'
        expected = {
            'action': 'TrainRan',
            'company': 'B&O',
            'train': '3',
            'amount': '90',
            'route': 'I15-H12-H10'
        }
        self.assertEqual(expected, company.runs_train(line))

    def test_pays_dividend(self):
        line = 'B&O pays out $50 = $5 per share ($30 to mpcoyne, $5 to riverfiend)'
        expected = {
            'action': 'DividendPayed',
            'company': 'B&O',
            'amount': '50',
            'per_share': '5'
        }
        self.assertEqual(expected, company.pays_dividend(line))

    def test_withholds(self):
        line = 'B&O withholds $80'
        expected = {
            'action': 'DividendWithheld',
            'company': 'B&O',
            'amount': '80'
        }
        self.assertEqual(expected, company.withholds(line))

    def test_skips_token(self):
        line = 'B&O skips place a token'
        expected = {
            'action': 'TokenSkipped',
            'company': 'B&O',
        }
        self.assertEqual(expected, company.skips_token(line))

    def test_skips_tile(self):
        line = 'B&O skips lay track'
        expected = {
            'action': 'TileSkipped',
            'company': 'B&O'
        }
        self.assertEqual(expected, company.skips_tile(line))

    def test_skips_run_train(self):
        line = 'B&O skips run routes'
        expected = {
            'action': 'TrainRunSkipped',
            'company': 'B&O',
        }
        self.assertEqual(expected, company.skips_run_train(line))

    def test_skips_buy_private(self):
        line = 'B&O skips buy companies'
        expected = {
            'action': 'PrivateBuySkipped',
            'company': 'B&O'
        }
        self.assertEqual(expected, company.skips_buy_private(line))

    def test_skips_buy_train(self):
        line = 'B&O skips buy trains'
        expected = {
            'action': 'TrainBuySkipped',
            'company': 'B&O',
        }
        self.assertEqual(expected, company.skips_buy_train(line))

    def test_does_not_run(self):
        line = 'B&O does not run'
        expected = {
            'action': 'DoesNotRun',
            'company': 'B&O',
        }
        self.assertEqual(expected, company.does_not_run(line))

    def test_discards_train(self):
        line = 'B&O discards 3'
        expected = {
            'action': 'TrainDiscarded',
            'company': 'B&O',
            'train': '3'
        }
        self.assertEqual(expected, company.discards_train(line))

    def test_exchanges_train(self):
        line = 'B&O exchanges a 4 for a D train for $800 from The Depot'
        expected = {
            'action': 'TrainExchanged',
            'company': 'B&O',
            'old_train': '4',
            'new_train': 'D',
            'amount': '800',
            'source': 'The Depot'
        }
        self.assertEqual(expected, company.exchanges_train(line))
