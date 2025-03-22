#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.events import market


class TestMarketEvents(unittest.TestCase):

    def test_share_price_moves(self):
        line = "B&O's share price moves right from $82 to $95"
        expected = {
            'event': 'SharePriceMove',
            'company': 'B&O',
            'direction': 'right',
            'share_price': '95'
        }
        self.assertEqual(expected, market.share_price_moves(line))
