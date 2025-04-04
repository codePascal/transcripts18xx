#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.patterns import actions


class BaseActionTest(unittest.TestCase):

    def assertMatch(self, action, line, expected):
        result = action.match(line)
        self.assertEqual(expected, result)


class TestActionHandler(BaseActionTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestPayOut(BaseActionTest):

    def test_match(self):
        line = 'B&O pays out $50 = $5 per share ($30 to player1, $5 to player2)'
        expected = dict(
            parent='Action',
            type='PayOut',
            company='B&O',
            amount='50',
            per_share='5',
        )
        self.assertMatch(actions.PayOut(), line, expected)


class TestWithhold(BaseActionTest):

    def test_match(self):
        line = 'B&O withholds $80'
        expected = dict(
            parent='Action',
            type='Withhold',
            company='B&O',
            amount='80',
        )
        self.assertMatch(actions.Withhold(), line, expected)


class TestBuyShare(BaseActionTest):

    def test_match(self):
        line = 'player1 buys a 20% share of B&O from the IPO for $200'
        expected = dict(
            parent='Action',
            type='BuyShare',
            player='player1',
            percentage='20',
            company='B&O',
            source='IPO',
            amount='200',
        )
        self.assertMatch(actions.BuyShare(), line, expected)


class TestSellShare(BaseActionTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestSellSingleShare(BaseActionTest):

    def test_match(self):
        line = 'player1 sells a 10% share of B&O and receives $67'
        expected = dict(
            parent='Action',
            type='SellShares',
            player='player1',
            percentage='10',
            company='B&O',
            amount='67',
        )
        self.assertMatch(actions.SellSingleShare(), line, expected)


class TestSellMultipleShares(BaseActionTest):

    def test_match(self):
        line = 'player1 sells 3 shares of B&O and receives $234'
        expected = dict(
            parent='Action',
            type='SellShares',
            player='player1',
            percentage='30',
            company='B&O',
            amount='234',
        )
        self.assertMatch(actions.SellMultipleShares(), line, expected)


class TestPass(BaseActionTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestNoValidActions(BaseActionTest):

    def test_match(self):
        line = 'player1 has no valid actions and passes'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.NoValidActions(), line, expected)


class TestRegularPass(BaseActionTest):

    def test_match(self):
        line = 'player1 passes'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.RegularPass(), line, expected)


class TestPassBuyPrivate(BaseActionTest):

    def test_match(self):
        line = 'player1 passes buy companies'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassBuyPrivate(), line, expected)


class TestPassAuction(BaseActionTest):

    def test_match(self):
        line = 'player1 passes on Camden & Amboy'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassAuction(), line, expected)


class TestPassTile(BaseActionTest):

    def test_match(self):
        line = 'player1 passes lay/upgrade track'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassTile(), line, expected)


class TestPassToken(BaseActionTest):

    def test_match(self):
        line = 'player1 passes place a token'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassToken(), line, expected)


class TestPassBuyTrain(BaseActionTest):

    def test_match(self):
        line = 'player1 passes buy trains'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassBuyTrain(), line, expected)


class TestSkip(BaseActionTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestDeclineSellShare(BaseActionTest):

    def test_match(self):
        line = 'player1 declines to sell shares'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.DeclineSellShare(), line, expected)


class TestDeclineBuyShare(BaseActionTest):

    def test_match(self):
        line = 'player1 declines to buy shares'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.DeclineBuyShare(), line, expected)


class TestSkipBuyPrivate(BaseActionTest):

    def test_match(self):
        line = 'player1 skips buy companies'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipBuyPrivate(), line, expected)


class TestSkipLayTile(BaseActionTest):

    def test_match(self):
        line = 'player1 skips lay track'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipLayTile(), line, expected)


class TestSkipPlaceToken(BaseActionTest):

    def test_match(self):
        line = 'player1 skips place a token'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipPlaceToken(), line, expected)


class TestSkipBuyTrain(BaseActionTest):

    def test_match(self):
        line = 'player1 skips buy trains'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipBuyTrain(), line, expected)


class TestSkipRunTrain(BaseActionTest):

    def test_match(self):
        line = 'player1 skips run routes'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipRunTrain(), line, expected)


class TestParCompany(BaseActionTest):

    def test_match(self):
        line = 'player1 pars C&O at $90'
        expected = dict(
            parent='Action',
            type='Par',
            player='player1',
            company='C&O',
            amount='90'
        )
        self.assertMatch(actions.ParCompany(), line, expected)


class TestBid(BaseActionTest):

    def test_match(self):
        line = 'player1 bids $150 for Mohawk & Hudson'
        expected = dict(
            parent='Action',
            type='Bid',
            player='player1',
            private='Mohawk & Hudson',
            amount='150'
        )
        self.assertMatch(actions.Bid(), line, expected)


class TestCollect(BaseActionTest):

    def test_match(self):
        line = 'player1 collects $20 from Mohawk & Hudson'
        expected = dict(
            parent='Action',
            type='Collect',
            entity='player1',
            source='Mohawk & Hudson',
            amount='20'
        )
        self.assertMatch(actions.Collect(), line, expected)


class TestBuyPrivate(BaseActionTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestBuyPrivateFromPlayer(BaseActionTest):

    def test_match(self):
        line = 'C&O buys Mohawk & Hudson from player1 for $240'
        expected = dict(
            parent='Action',
            type='BuyPrivate',
            source='player1',
            entity='C&O',
            private='Mohawk & Hudson',
            amount='240'
        )
        self.assertMatch(actions.BuyPrivateFromPlayer(), line, expected)


class TestBuyPrivateFromAuction(BaseActionTest):

    def test_match(self):
        line = 'player1 buys Mohawk & Hudson for $240'
        expected = dict(
            parent='Action',
            type='BuyPrivate',
            source='Auction',
            entity='player1',
            private='Mohawk & Hudson',
            amount='240'
        )
        self.assertMatch(actions.BuyPrivateFromAuction(), line, expected)


class TestWinAuctionAgainst(BaseActionTest):

    def test_match(self):
        line = 'player1 wins the auction for Mohawk & Hudson with a bid of $240'
        expected = dict(
            parent='Action',
            type='BuyPrivate',
            source='Auction',
            entity='player1',
            private='Mohawk & Hudson',
            amount='240'
        )
        self.assertMatch(actions.WinAuctionAgainst(), line, expected)


class TestWinAuction(BaseActionTest):

    def test_match(self):
        line = str(
            'player1 wins the auction for Mohawk & Hudson with the only bid of '
            '$240'
        )
        expected = dict(
            parent='Action',
            type='BuyPrivate',
            source='Auction',
            entity='player1',
            private='Mohawk & Hudson',
            amount='240'
        )
        self.assertMatch(actions.WinAuction(), line, expected)


class TestLayTile(BaseActionTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestLayTileForMoney(BaseActionTest):

    def test_match(self):
        line = str(
            'C&O spends $80 and lays tile #2 with rotation 0 on H15 (City)'
        )
        expected = dict(
            parent='Action',
            type='LayTile',
            company='C&O',
            amount='80',
            tile='2',
            rotation='0',
            location='H15 (City)'
        )
        self.assertMatch(actions.LayTileForMoney(), line, expected)


class TestLayTileForFree(BaseActionTest):

    def test_match(self):
        line = 'C&O lays tile #2 with rotation 0 on H15 (City)'
        expected = dict(
            parent='Action',
            type='LayTile',
            company='C&O',
            amount='0',
            tile='2',
            rotation='0',
            location='H15 (City)'
        )
        self.assertMatch(actions.LayTileForFree(), line, expected)


class TestPlaceToken(BaseActionTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestPlaceTokenForMoney(BaseActionTest):

    def test_match(self):
        line = 'C&O places a token on H15 (City) for $30'
        expected = dict(
            parent='Action',
            type='PlaceToken',
            company='C&O',
            amount='30',
            location='H15 (City)'
        )
        self.assertMatch(actions.PlaceTokenForMoney(), line, expected)


class TestPlaceTokenForFree(BaseActionTest):

    def test_match(self):
        line = 'C&O places a token on H15 (City)'
        expected = dict(
            parent='Action',
            type='PlaceToken',
            company='C&O',
            amount='0',
            location='H15 (City)'
        )
        self.assertMatch(actions.PlaceTokenForFree(), line, expected)


class TestBuyTrain(BaseActionTest):

    def test_match(self):
        line = 'C&O buys a D train for $800 from The Depot'
        expected = dict(
            parent='Action',
            type='BuyTrain',
            company='C&O',
            train='D',
            amount='800',
            source='The Depot'
        )
        self.assertMatch(actions.BuyTrain(), line, expected)


class TestRunTrain(BaseActionTest):

    def test_match(self):
        line = 'B&O runs a 6 train for $560: H15-H14-B13-E14-C13-B12'
        expected = dict(
            parent='Action',
            type='RunTrain',
            company='B&O',
            train='6',
            amount='560',
            route='H15-H14-B13-E14-C13-B12'
        )
        self.assertMatch(actions.RunTrain(), line, expected)


class TestDiscardTrain(BaseActionTest):

    def test_match(self):
        line = 'B&O discards 4'
        expected = dict(
            parent='Action',
            type='DiscardTrain',
            company='B&O',
            train='4'
        )
        self.assertMatch(actions.DiscardTrain(), line, expected)


class TestExchangeTrain(BaseActionTest):

    def test_match(self):
        line = 'C&O exchanges a 4 for a D train for $600 from The Depot'
        expected = dict(
            parent='Action',
            type='ExchangeTrain',
            company='C&O',
            old_train='4',
            new_train='D',
            amount='600',
            source='The Depot'
        )
        self.assertMatch(actions.ExchangeTrain(), line, expected)


class TestContribute(BaseActionTest):

    def test_match(self):
        line = 'player1 contributes $511'
        expected = dict(
            parent='Action',
            type='Contribute',
            player='player1',
            amount='511'
        )
        self.assertMatch(actions.Contribute(), line, expected)
