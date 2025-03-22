#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.events import phases


class TestPhasesEvents(unittest.TestCase):

    def test_phase_change(self):
        line = '-- Phase 2 (what all happens in Phase 2) --'
        expected = {
            'event': phases.PhaseEvents.NewPhase.name,
            'phase': '2'
        }
        self.assertEqual(expected, phases.new_phase(line))

    def test_bank_broke(self):
        line = '-- The bank has broken --'
        expected = {
            'event': phases.PhaseEvents.BankBroke.name
        }
        self.assertEqual(expected, phases.bank_broke(line))

    def test_game_over(self):
        line = '-- Game over: p1 ($40), p2 ($30), p3 ($20), p4 ($10) --'
        expected = {
            'event': phases.PhaseEvents.GameOver.name,
        }
        self.assertEqual(expected, phases.game_over(line))

    def test_operating_round(self):
        line = '-- Operating Round 1.2 (of 3) --'
        expected = {
            'event': phases.PhaseEvents.OperatingRound.name,
            'round': '1.2'
        }
        self.assertEqual(expected, phases.operating_round(line))

    def test_stock_round(self):
        line = '-- Stock Round 3 --'
        expected = {
            'event': phases.PhaseEvents.StockRound.name,
            'round': '3'
        }
        self.assertEqual(expected, phases.stock_round(line))
