#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import dividend


class TestDividendActions(unittest.TestCase):

    def test_full_pay(self):
        line = 'B&O pays out $50 = $5 per share ($30 to player1, $5 to player2)'
        expected = {
            'action': dividend.DividedActions.PayDivided.name,
            'company': 'B&O',
            'amount': '50',
            'per_share': '5'
        }
        self.assertEqual(expected, dividend.full_pay(line))

    def test_withhold(self):
        line = 'B&O withholds $80'
        expected = {
            'action': dividend.DividedActions.WithholdDivided.name,
            'company': 'B&O',
            'amount': '80'
        }
        self.assertEqual(expected, dividend.withhold(line))
