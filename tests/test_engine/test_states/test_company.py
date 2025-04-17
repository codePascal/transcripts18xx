#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.engine.states import company


class TestCompanyState(unittest.TestCase):

    def setUp(self) -> None:
        self.company = company.CompanyState(
            'company1', {'2': 0, '4': 0, 'D': 0}
        )

    def test_repr(self):
        self.assertEqual(
            str(
                "{'name': 'company1', 'cash': 0, 'privates': {}, "
                "'trains': {'2': 0, '4': 0, 'D': 0}, 'ipo': 10, 'market': 0, "
                "'president': None, 'share_price': 0}"
            ),
            self.company.__repr__()
        )

    def test_eval(self):
        rep = str(
            "{'name': 'company1', 'cash': 200, 'privates': {}, "
            "'trains': {'2': 1, '4': 3, 'D': 0}, 'ipo': 5, 'market': 2, "
            "'president': 'player1', 'share_price': 75}"
        )
        st = company.CompanyState.eval(rep)
        self.assertEqual('company1', st.name)
        self.assertEqual(200, st.cash)
        self.assertEqual(dict(), st.privates)
        self.assertEqual({'2': 1, '4': 3, 'D': 0}, st.trains)
        self.assertEqual(5, st.ipo)
        self.assertEqual(2, st.market)
        self.assertEqual('player1', st.president)
        self.assertEqual(75, st.share_price)

    def test__proc_train(self):
        self.assertEqual('4', company.CompanyState._proc_train(4.0))
        self.assertEqual('4', company.CompanyState._proc_train(4))
        self.assertEqual('4', company.CompanyState._proc_train('4'))
        self.assertEqual('D', company.CompanyState._proc_train('D'))

    def test_receives_dividend(self):
        self.company.market = 3
        self.company.receives_dividend('company1', 10)
        self.assertEqual(30, self.company.cash)

    def test_withholds(self):
        self.company.withholds(100)
        self.assertEqual(100, self.company.cash)

    def test_is_pared(self):
        self.company.is_pared(50)
        self.assertEqual(50, self.company.share_price)

    def test_lays_tile(self):
        self.company.lays_tile(0)
        self.assertEqual(0, self.company.cash)

        self.company.lays_tile(40)
        self.assertEqual(-40, self.company.cash)

    def test_places_token(self):
        self.company.places_token(0)
        self.assertEqual(0, self.company.cash)

        self.company.places_token(40)
        self.assertEqual(-40, self.company.cash)

    def test_buys_train(self):
        self.company.buys_train('4', 30)
        self.assertEqual(1, self.company.trains['4'])
        self.assertEqual(-30, self.company.cash)

    def test_discards_train(self):
        self.company.discards_train('4')
        self.assertEqual(-1, self.company.trains['4'])
        self.assertEqual(0, self.company.cash)

    def test_exchanges_train(self):
        self.company.exchanges_train('4', 'D', 40)
        self.assertEqual(-1, self.company.trains['4'])
        self.assertEqual(1, self.company.trains['D'])
        self.assertEqual(-40, self.company.cash)

    def test_receives_funds(self):
        self.company.receives_funds(100)
        self.assertEqual(100, self.company.cash)

    def test_share_price_moves(self):
        self.company.share_price_moves(60)
        self.assertEqual(60, self.company.share_price)

    def test_president_assignment(self):
        self.company.president_assignment('player1')
        self.assertEqual('player1', self.company.president)

    def test_trains_rust(self):
        self.company.trains['4'] = 3
        self.company.trains_rust('4')
        self.assertEqual(0, self.company.trains['4'])


class TestCompanies(unittest.TestCase):

    def setUp(self) -> None:
        self.companies = company.Companies(
            ['company1', 'company2'], ['2', '3', 'D']
        )

    def test_repr(self):
        self.assertEqual(
            str(
                "{'name': 'company1', 'cash': 0, 'privates': {}, "
                "'trains': {'2': 0, '3': 0, 'D': 0}, 'ipo': 10, 'market': 0, "
                "'president': None, 'share_price': 0}\n"
                "{'name': 'company2', 'cash': 0, 'privates': {}, "
                "'trains': {'2': 0, '3': 0, 'D': 0}, 'ipo': 10, 'market': 0, "
                "'president': None, 'share_price': 0}\n"
            ),
            self.companies.__repr__()
        )

    def test_share_prices(self):
        self.companies.states[0].share_price = 50
        self.companies.states[1].share_price = 40
        self.assertEqual(
            dict(company1=50, company2=40), self.companies.share_prices()
        )
