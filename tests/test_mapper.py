#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx import mapper


class TestPatternMatcher(unittest.TestCase):

    def setUp(self) -> None:
        self.cls = mapper.PatternMatcher()

    def test__get_patterns(self):
        subclasses = self.cls._get_patterns()
        self.assertEqual(56, len(subclasses))

    def test__select(self):
        search = [None, None, dict(key=1, name='Mario'), None, None]
        result = self.cls._select(search, str())
        self.assertIsInstance(result, dict)
        self.assertEqual(dict(key=1, name='Mario'), result)

    def test__select_exception(self):
        search = [None, None, dict(key=1), None, dict(key=2)]
        with self.assertRaises(ValueError) as e:
            self.cls._select(search, 'example line')
        expected = str(
            "Multiple matches found for line `example line`:\n"
            "{'key': 1}\n"
            "{'key': 2}"
        )
        self.assertEqual(expected, e.exception.__str__())

    def test__search_action(self):
        line = 'player1 buys a 20% share of B&O from the IPO for $200'
        result = self.cls._search(line)
        self.assertEqual(55, len([r for r in result if r is None]))
        self.assertEqual(1, len([r for r in result if isinstance(r, dict)]))

    def test__search_event(self):
        line = "B&O's share price moves right from $67 to $70"
        result = self.cls._search(line)
        self.assertEqual(55, len([r for r in result if r is None]))
        self.assertEqual(1, len([r for r in result if isinstance(r, dict)]))

    def test_run_action(self):
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
        result = self.cls.run(line)
        self.assertEqual(expected, result)

    def test_run_event(self):
        line = "B&O's share price moves right from $67 to $70"
        expected = dict(
            parent='Event',
            type='SharePriceMoves',
            company='B&O',
            direction='right',
            share_price='70'
        )
        result = self.cls.run(line)
        self.assertEqual(expected, result)

    def test_run_pass(self):
        line = 'player1 passes on Mohawk & Hudson'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1',
        )
        result = self.cls.run(line)
        self.assertEqual(expected, result)
