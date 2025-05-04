#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transcripts18xx.engine.steps import events

from tests.test_engine.test_steps.test_step import BaseStepTest


class TestEventStep(BaseStepTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestReceiveShare(BaseStepTest):

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

    def test_state_update_from_private(self):
        players, companies = self.game_state()
        row = self.row()
        row.company = 'company2'
        row.player = 'player1'
        row.percentage = 10
        self.invoke_state_update(events.ReceiveShare(), row, players, companies)

        p = players.get('player1')
        self.assertEqual(1000, p.cash)
        self.assertEqual(dict(), p.privates)
        self.assertEqual(1000, p.value)  # value not updated yet in pipeline
        self.assertEqual(dict(company1=0, company2=1, company3=0), p.shares)
        self.assertFalse(p.priority_deal)

        c = companies.get('company2')
        self.assertEqual(0, c.cash)
        self.assertEqual(dict(), c.privates)
        self.assertEqual(
            {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}, c.trains
        )
        self.assertEqual(9, c.ipo)
        self.assertEqual(0, c.market)
        self.assertEqual(None, c.president)
        self.assertEqual(0, c.share_price)

        self.assertDefaultPlayer(players, 'player2')
        self.assertDefaultPlayer(players, 'player3')
        self.assertDefaultCompany(companies, 'company1')
        self.assertDefaultCompany(companies, 'company3')


class TestReceiveFunds(BaseStepTest):

    def test_match(self):
        line = 'C&O receives $300'
        expected = dict(
            parent='Event',
            type='ReceiveFunds',
            company='C&O',
            amount='300'
        )
        self.assertMatch(events.ReceiveFunds(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestCompanyFloats(BaseStepTest):

    def test_match(self):
        line = 'C&O floats'
        expected = dict(
            parent='Event',
            type='CompanyFloats',
            company='C&O',
        )
        self.assertMatch(events.CompanyFloats(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestSelectsHome(BaseStepTest):

    def test_match(self):
        line = 'B&O must choose city for token'
        expected = dict(
            parent='Event',
            type='SelectsHome',
            company='B&O',
        )
        self.assertMatch(events.SelectsHome(), line, expected)


class TestDoesNotRun(BaseStepTest):

    def test_match(self):
        line = 'C&O does not run'
        expected = dict(
            parent='Event',
            type='DoesNotRun',
            company='C&O',
        )
        self.assertMatch(events.DoesNotRun(), line, expected)


class TestSharePriceMove(BaseStepTest):

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

    def test_state_update(self):
        # TODO
        pass


class TestNewPhase(BaseStepTest):

    def test_match(self):
        line = '-- Phase 3 (blabla) --'
        expected = dict(
            parent='Event',
            type='NewPhase',
            phase='3'
        )
        self.assertMatch(events.NewPhase(), line, expected)


class TestBankBroke(BaseStepTest):

    def test_match(self):
        line = '-- The bank has broken --'
        expected = dict(
            parent='Event',
            type='BankBroke'
        )
        self.assertMatch(events.BankBroke(), line, expected)


class TestGameOver(BaseStepTest):

    def test_match(self):
        line = '-- Game over: player1 ($200), player3 ($100), player2 ($50) --'
        expected = dict(
            parent='Event',
            type='GameOver',
            result="{'player1': 200, 'player3': 100, 'player2': 50}"
        )
        self.assertMatch(events.GameOver(), line, expected)


class TestOperatingRound(BaseStepTest):

    def test_match(self):
        line = '-- Operating Round 3.2 (of 2) --'
        expected = dict(
            parent='Event',
            type='OperatingRound',
            sequence='OR 3.2'
        )
        self.assertMatch(events.OperatingRound(), line, expected)


class TestStockRound(BaseStepTest):

    def test_match(self):
        line = '-- Stock Round 4 --'
        expected = dict(
            parent='Event',
            type='StockRound',
            sequence='SR 4'
        )
        self.assertMatch(events.StockRound(), line, expected)


class TestPresidentNomination(BaseStepTest):

    def test_match(self):
        line = 'player1 becomes the president of B&O'
        expected = dict(
            parent='Event',
            type='PresidentNomination',
            player='player1',
            company='B&O'
        )
        self.assertMatch(events.PresidentNomination(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestPriorityDeal(BaseStepTest):

    def test_match(self):
        line = 'player1 has priority deal'
        expected = dict(
            parent='Event',
            type='PriorityDeal',
            player='player1',
        )
        self.assertMatch(events.PriorityDeal(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestOperatesCompany(BaseStepTest):

    def test_match(self):
        line = 'player1 operates B&O'
        expected = dict(
            parent='Event',
            type='OperatesCompany',
            player='player1',
            company='B&O'
        )
        self.assertMatch(events.OperatesCompany(), line, expected)


class TestAllPrivatesClose(BaseStepTest):

    def test_match(self):
        line = '-- Event: Private companies close'
        expected = dict(
            parent='Event',
            type='AllPrivatesClose',
        )
        self.assertMatch(events.AllPrivatesClose(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestPrivateCloses(BaseStepTest):

    def test_match(self):
        line = 'Mohawk & Hudson closes'
        expected = dict(
            parent='Event',
            type='PrivateCloses',
            private='Mohawk & Hudson'
        )
        self.assertMatch(events.PrivateCloses(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestPrivateAuctioned(BaseStepTest):

    def test_match(self):
        line = 'Mohawk & Hudson goes up for auction'
        expected = dict(
            parent='Event',
            type='PrivateAuctioned',
            private='Mohawk & Hudson'
        )
        self.assertMatch(events.PrivateAuctioned(), line, expected)


class TestTrainsRust(BaseStepTest):

    def test_match(self):
        line = '-- Event: 4 trains rust'
        expected = dict(
            parent='Event',
            type='TrainsRust',
            train='4'
        )
        self.assertMatch(events.TrainsRust(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestPlayerGoesBankrupt(BaseStepTest):

    def test_match(self):
        line = '-- player1 goes bankrupt and sells remaining shares --'
        expected = dict(
            parent='Event',
            type='PlayerGoesBankrupt',
            player='player1'
        )
        self.assertMatch(events.PlayerGoesBankrupt(), line, expected)

    def test_state_update(self):
        # TODO
        pass
