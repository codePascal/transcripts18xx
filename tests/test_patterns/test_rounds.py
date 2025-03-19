#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import rounds


class TestRoundsPattern(unittest.TestCase):

    def test_phase(self):
        line = ' -- Phase 1'
        ret = rounds.phase(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Phase Change', ret['event'])
        self.assertEqual('1', ret['phase'])

    def test_operating_round(self):
        line = '-- Operating Round 1.1'
        ret = rounds.operating_round(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Operating Round', ret['event'])
        self.assertEqual('1.1', ret['round'])

    def test_stock_round(self):
        line = '-- Stock Round 1.1'
        ret = rounds.stock_round(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Stock Round', ret['event'])
        self.assertEqual('1.1', ret['round'])

    def test_merger_and_conversion_round(self):
        line = '-- Merger and Conversion Round 1.1'
        ret = rounds.merger_and_conversion(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Merger and Conversion Round', ret['event'])
        self.assertEqual('1.1', ret['round'])

    def test_acquisition_round(self):
        line = '-- Acquisition Round 1.1'
        ret = rounds.acquisition(line)
        self.assertIsInstance(ret, dict)
        self.assertEqual('Acquisition Round', ret['event'])
        self.assertEqual('1.1', ret['round'])
