#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transcripts18xx.patterns import events

from tests.test_patterns.test_pattern import BasePatternTest


class TestEventHandler(BasePatternTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestReceiveShare(BasePatternTest):

    def test_match(self):
        line = 'player1 receives a 20% share of B&O'
        expected = dict(
            parent='Event',
            type='ReceiveShare',
            company='B&O',
            player='player1',
            percentage='20'
        )
        self.assertMatch(events.ReceiveShare(), line, expected)


class TestReceiveFunds(BasePatternTest):

    def test_match(self):
        line = 'C&O receives $300'
        expected = dict(
            parent='Event',
            type='ReceiveFunds',
            company='C&O',
            amount='300'
        )
        self.assertMatch(events.ReceiveFunds(), line, expected)


class TestCompanyFloats(BasePatternTest):

    def test_match(self):
        line = 'C&O floats'
        expected = dict(
            parent='Event',
            type='CompanyFloats',
            company='C&O',
        )
        self.assertMatch(events.CompanyFloats(), line, expected)


class TestSelectsHome(BasePatternTest):

    def test_match(self):
        line = 'B&O must choose city for token'
        expected = dict(
            parent='Event',
            type='SelectsHome',
            company='B&O',
        )
        self.assertMatch(events.SelectsHome(), line, expected)


class TestDoesNotRun(BasePatternTest):

    def test_match(self):
        line = 'C&O does not run'
        expected = dict(
            parent='Event',
            type='DoesNotRun',
            company='C&O',
        )
        self.assertMatch(events.DoesNotRun(), line, expected)


class TestSharePriceMove(BasePatternTest):

    def test_match(self):
        line = "B&O's share price moves right from $67 to $70"
        expected = dict(
            parent='Event',
            type='SharePriceMoves',
            company='B&O',
            direction='right',
            share_price='70'
        )
        self.assertMatch(events.SharePriceMove(), line, expected)


class TestNewPhase(BasePatternTest):

    def test_match(self):
        line = '-- Phase 3 (blabla) --'
        expected = dict(
            parent='Event',
            type='NewPhase',
            phase='3'
        )
        self.assertMatch(events.NewPhase(), line, expected)


class TestBankBroke(BasePatternTest):

    def test_match(self):
        line = '-- The bank has broken --'
        expected = dict(
            parent='Event',
            type='BankBroke'
        )
        self.assertMatch(events.BankBroke(), line, expected)


class TestGameOver(BasePatternTest):

    def test_match(self):
        line = '-- Game over: (ranking...)'
        expected = dict(
            parent='Event',
            type='GameOver',
        )
        self.assertMatch(events.GameOver(), line, expected)


class TestOperatingRound(BasePatternTest):

    def test_match(self):
        line = '-- Operating Round 3.2 (of 2) --'
        expected = dict(
            parent='Event',
            type='OperatingRound',
            round='OR 3.2'
        )
        self.assertMatch(events.OperatingRound(), line, expected)


class TestStockRound(BasePatternTest):

    def test_match(self):
        line = '-- Stock Round 4 --'
        expected = dict(
            parent='Event',
            type='StockRound',
            round='SR 4'
        )
        self.assertMatch(events.StockRound(), line, expected)


class TestPresidentNomination(BasePatternTest):

    def test_match(self):
        line = 'player1 becomes the president of B&O'
        expected = dict(
            parent='Event',
            type='PresidentNomination',
            player='player1',
            company='B&O'
        )
        self.assertMatch(events.PresidentNomination(), line, expected)


class TestPriorityDeal(BasePatternTest):

    def test_match(self):
        line = 'player1 has priority deal'
        expected = dict(
            parent='Event',
            type='PriorityDeal',
            player='player1',
        )
        self.assertMatch(events.PriorityDeal(), line, expected)


class TestOperatesCompany(BasePatternTest):

    def test_match(self):
        line = 'player1 operates B&O'
        expected = dict(
            parent='Event',
            type='OperatesCompany',
            player='player1',
            company='B&O'
        )
        self.assertMatch(events.OperatesCompany(), line, expected)


class TestAllPrivatesClose(BasePatternTest):

    def test_match(self):
        line = '-- Event: Private companies close'
        expected = dict(
            parent='Event',
            type='AllPrivatesClose',
        )
        self.assertMatch(events.AllPrivatesClose(), line, expected)


class TestPrivateCloses(BasePatternTest):

    def test_match(self):
        line = 'Mohawk & Hudson closes'
        expected = dict(
            parent='Event',
            type='PrivateCloses',
            private='Mohawk & Hudson'
        )
        self.assertMatch(events.PrivateCloses(), line, expected)


class TestPrivateAuctioned(BasePatternTest):

    def test_match(self):
        line = 'Mohawk & Hudson goes up for auction'
        expected = dict(
            parent='Event',
            type='PrivateAuctioned',
            private='Mohawk & Hudson'
        )
        self.assertMatch(events.PrivateAuctioned(), line, expected)


class TestTrainsRust(BasePatternTest):

    def test_match(self):
        line = '-- Event: 4 trains rust'
        expected = dict(
            parent='Event',
            type='TrainsRust',
            train='4'
        )
        self.assertMatch(events.TrainsRust(), line, expected)
