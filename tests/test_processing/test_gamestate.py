#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from transcripts18xx.processing.gamestate import GameStateProcessor
from transcripts18xx.games import Game1830
from transcripts18xx.engine.states.player import PlayerState
from transcripts18xx.engine.states.company import CompanyState

from tests import context


# TODO: add company states for ISR 1 and game over


class TestGameStateProcessor1830(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        df = pd.read_csv(context.processed_transcript_1830())
        gsp = GameStateProcessor(df, Game1830())
        gsp.generate()
        cls.df = gsp.save_to_dataframe(context.transcript_1830())

    def test_isr_1(self):
        isr1 = self.df[self.df.sequence == 'ISR 1']
        final_states = isr1.iloc[-1, :]

        mpakfm = PlayerState.eval(final_states.mpakfm)
        self.assertEqual(560, mpakfm.cash)
        self.assertEqual(600, mpakfm.value)
        self.assertEqual(0, sum(mpakfm.shares.values()))
        self.assertFalse(mpakfm.priority_deal)
        self.assertEqual({'Champlain & St.Lawrence': 40}, mpakfm.privates)

        mpcoyne = PlayerState.eval(final_states.mpcoyne)
        self.assertEqual(360, mpcoyne.cash)
        self.assertEqual(780, mpcoyne.value)
        self.assertEqual(2, sum(mpcoyne.shares.values()))
        self.assertEqual(2, mpcoyne.shares['B&O'])
        self.assertFalse(mpcoyne.priority_deal)
        self.assertEqual(
            {'Schuylkill Valley': 20, 'Baltimore & Ohio': 220}, mpcoyne.privates
        )

        riverfiend = PlayerState.eval(final_states.riverfiend)
        self.assertEqual(525, riverfiend.cash)
        self.assertEqual(595, riverfiend.value)
        self.assertEqual(0, sum(riverfiend.shares.values()))
        self.assertTrue(riverfiend.priority_deal)
        self.assertEqual({'Delaware & Hudson': 70}, riverfiend.privates)

        leesin = PlayerState.eval(final_states.leesin)
        self.assertEqual(250, leesin.cash)
        self.assertEqual(520, leesin.value)
        self.assertEqual(1, sum(leesin.shares.values()))
        self.assertEqual(1, leesin.shares['PRR'])
        self.assertFalse(leesin.priority_deal)
        self.assertEqual(
            {'Mohawk & Hudson': 110, 'Camden & Amboy': 160}, leesin.privates
        )

    def test_game_over(self):
        last_round = self.df[self.df.sequence == 'OR 8.3']
        final_states = last_round.iloc[-1, :]

        # TODO: enable priority deal when fixed

        mpakfm = PlayerState.eval(final_states.mpakfm)
        self.assertEqual(1260, mpakfm.cash)
        self.assertEqual(2740, mpakfm.value)
        self.assertEqual(8, sum(mpakfm.shares.values()))
        self.assertEqual(2, mpakfm.shares['B&O'])
        self.assertEqual(0, mpakfm.shares['B&M'])
        self.assertEqual(0, mpakfm.shares['ERIE'])
        self.assertEqual(0, mpakfm.shares['PRR'])
        self.assertEqual(6, mpakfm.shares['NYC'])
        self.assertEqual(0, mpakfm.shares['C&O'])
        self.assertEqual(0, mpakfm.shares['NYNH'])
        self.assertEqual(0, mpakfm.shares['CPR'])
        self.assertTrue(mpakfm.priority_deal)
        self.assertEqual(dict(), mpakfm.privates)

        mpcoyne = PlayerState.eval(final_states.mpcoyne)
        self.assertEqual(3304, mpcoyne.cash)
        self.assertEqual(6735, mpcoyne.value)
        self.assertEqual(19, sum(mpcoyne.shares.values()))
        self.assertEqual(6, mpcoyne.shares['B&O'])
        self.assertEqual(6, mpcoyne.shares['B&M'])
        self.assertEqual(4, mpcoyne.shares['ERIE'])
        self.assertEqual(1, mpcoyne.shares['PRR'])
        self.assertEqual(1, mpcoyne.shares['NYC'])
        self.assertEqual(1, mpcoyne.shares['C&O'])
        self.assertEqual(0, mpcoyne.shares['NYNH'])
        self.assertEqual(0, mpcoyne.shares['CPR'])
        self.assertFalse(mpcoyne.priority_deal)
        self.assertEqual(dict(), mpcoyne.privates)

        riverfiend = PlayerState.eval(final_states.riverfiend)
        self.assertEqual(3560, riverfiend.cash)
        self.assertEqual(5523, riverfiend.value)
        self.assertEqual(19, sum(riverfiend.shares.values()))
        self.assertEqual(0, riverfiend.shares['B&O'])
        self.assertEqual(3, riverfiend.shares['B&M'])
        self.assertEqual(6, riverfiend.shares['ERIE'])
        self.assertEqual(1, riverfiend.shares['PRR'])
        self.assertEqual(1, riverfiend.shares['NYC'])
        self.assertEqual(6, riverfiend.shares['C&O'])
        self.assertEqual(2, riverfiend.shares['NYNH'])
        self.assertEqual(0, riverfiend.shares['CPR'])
        self.assertFalse(riverfiend.priority_deal)
        self.assertEqual(dict(), riverfiend.privates)

        leesin = PlayerState.eval(final_states.leesin)
        self.assertEqual(3432, leesin.cash)
        self.assertEqual(6648, leesin.value)
        self.assertEqual(26, sum(leesin.shares.values()))
        self.assertEqual(2, leesin.shares['B&O'])
        self.assertEqual(1, leesin.shares['B&M'])
        self.assertEqual(0, leesin.shares['ERIE'])
        self.assertEqual(8, leesin.shares['PRR'])
        self.assertEqual(2, leesin.shares['NYC'])
        self.assertEqual(1, leesin.shares['C&O'])
        self.assertEqual(6, leesin.shares['NYNH'])
        self.assertEqual(6, leesin.shares['CPR'])
        self.assertFalse(leesin.priority_deal)
        self.assertEqual(dict(), leesin.privates)
