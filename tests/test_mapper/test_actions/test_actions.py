#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import actions


class TestActions(unittest.TestCase):

    def test_common_actions(self):
        line = "leesin receives a 10% share of PRR"
        results = actions.actions(line)
        self.assertTrue(
            any(r and r.get("action") == "ShareReceived" for r in results)
        )

    def test_company_actions(self):
        line = "NYNH places a token on G19"
        results = actions.actions(line)
        self.assertTrue(
            any(r and r.get("action") == "TokenPlaced" for r in results)
        )

    def test_player_actions(self):
        line = "riverfiend bids $170 for Camden & Amboy"
        results = actions.actions(line)
        self.assertTrue(
            any(r and r.get("action") == "BidPlaced" for r in results)
        )

    def test_none(self):
        line = "this line should not match anything"
        results = actions.actions(line)
        self.assertTrue(all(r is None for r in results))
