#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transcripts18xx.engine.steps import actions

from tests.test_engine.test_steps.test_step import BaseStepTest


class TestActionStep(BaseStepTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestPayOut(BaseStepTest):

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

    def test_state_update(self):
        players, companies = self.game_state()
        players.states[0].shares['company1'] = 2
        players.states[1].shares['company1'] = 1
        players.states[2].shares['company1'] = 4
        companies.states[0].market = 2

        row = self.row()
        row.company = 'company1'
        row.amount = 50
        row.per_share = 5
        self.invoke_state_update(actions.PayOut(), row, players, companies)

        p1 = players.get('player1')
        self.assertEqual(1010, p1.cash)
        self.assertEqual(dict(), p1.privates)
        self.assertEqual(1010, p1.value)
        self.assertEqual(dict(company1=2, company2=0, company3=0), p1.shares)
        self.assertFalse(p1.priority_deal)

        p2 = players.get('player2')
        self.assertEqual(1005, p2.cash)
        self.assertEqual(dict(), p2.privates)
        self.assertEqual(1005, p2.value)
        self.assertEqual(dict(company1=1, company2=0, company3=0), p2.shares)
        self.assertFalse(p2.priority_deal)

        p3 = players.get('player3')
        self.assertEqual(1020, p3.cash)
        self.assertEqual(dict(), p3.privates)
        self.assertEqual(1020, p3.value)
        self.assertEqual(dict(company1=4, company2=0, company3=0), p3.shares)
        self.assertFalse(p3.priority_deal)

        c = companies.get('company1')
        self.assertEqual(10, c.cash)
        self.assertEqual(dict(), c.privates)
        self.assertEqual(
            {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}, c.trains
        )
        self.assertEqual(10, c.ipo)
        self.assertEqual(2, c.market)
        self.assertEqual(None, c.president)
        self.assertEqual(0, c.share_price)

        self.assertDefaultCompany(companies, 'company2')
        self.assertDefaultCompany(companies, 'company3')


class TestWithhold(BaseStepTest):

    def test_match(self):
        line = 'B&O withholds $80'
        expected = dict(
            parent='Action',
            type='Withhold',
            company='B&O',
            amount='80',
        )
        self.assertMatch(actions.Withhold(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestBuyShare(BaseStepTest):

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

    def test_state_update(self):
        # TODO
        pass


class TestSellShare(BaseStepTest):

    def test_match(self):
        # Skip abstract class
        pass

    def test_state_update(self):
        # TODO
        pass


class TestSellSingleShare(BaseStepTest):

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


class TestSellMultipleShares(BaseStepTest):

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


class TestPass(BaseStepTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestNoValidActions(BaseStepTest):

    def test_match(self):
        line = 'player1 has no valid actions and passes'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.NoValidActions(), line, expected)


class TestRegularPass(BaseStepTest):

    def test_match(self):
        line = 'player1 passes'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.RegularPass(), line, expected)


class TestPassBuyPrivate(BaseStepTest):

    def test_match(self):
        line = 'player1 passes buy companies'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassBuyPrivate(), line, expected)


class TestPassAuction(BaseStepTest):

    def test_match(self):
        line = 'player1 passes on Camden & Amboy'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassAuction(), line, expected)


class TestPassTile(BaseStepTest):

    def test_match(self):
        line = 'player1 passes lay/upgrade track'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassTile(), line, expected)


class TestPassToken(BaseStepTest):

    def test_match(self):
        line = 'player1 passes place a token'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassToken(), line, expected)


class TestPassBuyTrain(BaseStepTest):

    def test_match(self):
        line = 'player1 passes buy trains'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1'
        )
        self.assertMatch(actions.PassBuyTrain(), line, expected)


class TestSkip(BaseStepTest):

    def test_match(self):
        # Skip abstract class
        pass


class TestDeclineSellShare(BaseStepTest):

    def test_match(self):
        line = 'player1 declines to sell shares'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.DeclineSellShare(), line, expected)


class TestDeclineBuyShare(BaseStepTest):

    def test_match(self):
        line = 'player1 declines to buy shares'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.DeclineBuyShare(), line, expected)


class TestSkipBuyPrivate(BaseStepTest):

    def test_match(self):
        line = 'player1 skips buy companies'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipBuyPrivate(), line, expected)


class TestSkipLayTile(BaseStepTest):

    def test_match(self):
        line = 'player1 skips lay track'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipLayTile(), line, expected)


class TestSkipPlaceToken(BaseStepTest):

    def test_match(self):
        line = 'player1 skips place a token'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipPlaceToken(), line, expected)


class TestSkipBuyTrain(BaseStepTest):

    def test_match(self):
        line = 'player1 skips buy trains'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipBuyTrain(), line, expected)


class TestSkipRunTrain(BaseStepTest):

    def test_match(self):
        line = 'player1 skips run routes'
        expected = dict(
            parent='Action',
            type='Skip',
            entity='player1'
        )
        self.assertMatch(actions.SkipRunTrain(), line, expected)


class TestParCompany(BaseStepTest):

    def test_match(self):
        line = 'player1 pars C&O at $90'
        expected = dict(
            parent='Action',
            type='Par',
            player='player1',
            company='C&O',
            share_price='90'
        )
        self.assertMatch(actions.ParCompany(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestBid(BaseStepTest):

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


class TestCollect(BaseStepTest):

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

    def test_state_update(self):
        # TODO
        pass


class TestBuyPrivate(BaseStepTest):

    def test_state_update_from_auction_at_face_value(self):
        players, companies = self.game_state()
        row = self.row()
        row.player = 'player1'
        row.amount = 40
        row.private = 'private2'
        self.invoke_state_update(actions.BuyPrivate(), row, players, companies)

        p = players.get('player1')
        self.assertEqual(960, p.cash)
        self.assertEqual(dict(private2=40), p.privates)
        self.assertEqual(1000, p.value)
        self.assertEqual(dict(company1=0, company2=0, company3=0), p.shares)
        self.assertFalse(p.priority_deal)

        self.assertDefaultPlayer(players, 'player2')
        self.assertDefaultPlayer(players, 'player3')
        self.assertDefaultCompany(companies, 'company1')
        self.assertDefaultCompany(companies, 'company2')
        self.assertDefaultCompany(companies, 'company3')

    def test_state_update_from_auction_more_than_face_value(self):
        players, companies = self.game_state()
        row = self.row()
        row.player = 'player1'
        row.amount = 60
        row.private = 'private2'
        self.invoke_state_update(actions.BuyPrivate(), row, players, companies)

        p = players.get('player1')
        self.assertEqual(940, p.cash)
        self.assertEqual(dict(private2=40), p.privates)
        self.assertEqual(1000, p.value)  # value not updated yet in pipeline
        self.assertEqual(dict(company1=0, company2=0, company3=0), p.shares)
        self.assertFalse(p.priority_deal)

        self.assertDefaultPlayer(players, 'player2')
        self.assertDefaultPlayer(players, 'player3')
        self.assertDefaultCompany(companies, 'company1')
        self.assertDefaultCompany(companies, 'company2')
        self.assertDefaultCompany(companies, 'company3')

    def test_state_update_from_auction_less_than_face_value(self):
        players, companies = self.game_state()
        row = self.row()
        row.player = 'player1'
        row.amount = 30
        row.private = 'private2'
        self.invoke_state_update(actions.BuyPrivate(), row, players, companies)

        p = players.get('player1')
        self.assertEqual(970, p.cash)
        self.assertEqual(dict(private2=40), p.privates)
        self.assertEqual(1000, p.value)  # value not updated yet in pipeline
        self.assertEqual(dict(company1=0, company2=0, company3=0), p.shares)
        self.assertFalse(p.priority_deal)

        self.assertDefaultPlayer(players, 'player2')
        self.assertDefaultPlayer(players, 'player3')
        self.assertDefaultCompany(companies, 'company1')
        self.assertDefaultCompany(companies, 'company2')
        self.assertDefaultCompany(companies, 'company3')

    def test_state_update_from_player(self):
        players, companies = self.game_state()
        row = self.row()
        row.company = 'company1'
        row.amount = 240
        row.source = 'player2'
        row.private = 'private3'
        players.states[1].privates['private3'] = 70
        self.invoke_state_update(actions.BuyPrivate(), row, players, companies)

        p = players.get('player2')
        self.assertEqual(1240, p.cash)
        self.assertEqual(dict(), p.privates)
        self.assertEqual(1000, p.value)  # value not updated yet in pipeline
        self.assertEqual(dict(company1=0, company2=0, company3=0), p.shares)
        self.assertFalse(p.priority_deal)

        c = companies.get('company1')
        self.assertEqual(-240, c.cash)
        self.assertEqual(dict(private3=70), c.privates)
        self.assertEqual(
            {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'D': 0}, c.trains
        )
        self.assertEqual(10, c.ipo)
        self.assertEqual(0, c.market)
        self.assertEqual(None, c.president)
        self.assertEqual(0, c.share_price)

        self.assertDefaultPlayer(players, 'player1')
        self.assertDefaultPlayer(players, 'player3')
        self.assertDefaultCompany(companies, 'company2')
        self.assertDefaultCompany(companies, 'company3')


class TestBuyPrivateFromPlayer(BaseStepTest):

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


class TestBuyPrivateFromAuction(BaseStepTest):

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


class TestWinAuctionAgainst(BaseStepTest):

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


class TestWinAuction(BaseStepTest):

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


class TestLayTile(BaseStepTest):

    def test_match(self):
        # Skip abstract class
        pass

    def test_state_update(self):
        # TODO
        pass


class TestLayTileForMoney(BaseStepTest):

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


class TestLayTileForFree(BaseStepTest):

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


class TestPlaceToken(BaseStepTest):

    def test_match(self):
        # Skip abstract class
        pass

    def test_state_update(self):
        # TODO
        pass


class TestPlaceTokenForMoney(BaseStepTest):

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


class TestPlaceTokenForFree(BaseStepTest):

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


class TestBuyTrain(BaseStepTest):

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

    def test_state_update(self):
        # TODO
        pass


class TestRunTrain(BaseStepTest):

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


class TestDiscardTrain(BaseStepTest):

    def test_match(self):
        line = 'B&O discards 4'
        expected = dict(
            parent='Action',
            type='DiscardTrain',
            company='B&O',
            train='4'
        )
        self.assertMatch(actions.DiscardTrain(), line, expected)

    def test_state_update(self):
        # TODO
        pass


class TestExchangeTrain(BaseStepTest):

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

    def test_state_update(self):
        # TODO
        pass


class TestContribute(BaseStepTest):

    def test_match(self):
        line = 'player1 contributes $511'
        expected = dict(
            parent='Action',
            type='Contribute',
            player='player1',
            amount='511'
        )
        self.assertMatch(actions.Contribute(), line, expected)

    def test_state_update(self):
        # TODO
        pass
