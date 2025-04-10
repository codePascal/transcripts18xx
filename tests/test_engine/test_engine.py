#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.engine import engine


class TestEngineSteps(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.pattern = engine.EngineSteps()

    def test__patterns(self):
        subclasses = self.pattern._patterns()
        self.assertEqual(61, len(subclasses))

    def test_patterns(self):
        subclasses = self.pattern.patterns()
        self.assertEqual(59, len(subclasses))


class TestLineParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.matcher = engine.LineParser()

    def test__select(self):
        search = [None, None, dict(key=1, name='Mario'), None, None]
        result = self.matcher._select(search, str())
        self.assertIsInstance(result, dict)
        self.assertEqual(dict(key=1, name='Mario'), result)

    def test__select_exception(self):
        search = [None, None, dict(key=1), None, dict(key=2)]
        with self.assertRaises(ValueError) as e:
            self.matcher._select(search, 'example line')
        expected = str(
            "Multiple matches found for line `example line`:\n"
            "{'key': 1}\n"
            "{'key': 2}"
        )
        self.assertEqual(expected, e.exception.__str__())

    def test__search_action(self):
        line = 'player1 buys a 20% share of B&O from the IPO for $200'
        result = self.matcher._search(line)
        self.assertEqual(58, len([r for r in result if r is None]))
        self.assertEqual(1, len([r for r in result if isinstance(r, dict)]))

    def test__search_event(self):
        line = "B&O's share price moves right from $67 to $70"
        result = self.matcher._search(line)
        self.assertEqual(58, len([r for r in result if r is None]))
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
        result = self.matcher.run(line)
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
        result = self.matcher.run(line)
        self.assertEqual(expected, result)

    def test_run_pass(self):
        line = 'player1 passes on Mohawk & Hudson'
        expected = dict(
            parent='Action',
            type='Pass',
            entity='player1',
        )
        result = self.matcher.run(line)
        self.assertEqual(expected, result)


class TestStepMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mapper = engine.StepMapper()

    def test__search(self):
        step = self.mapper._search(engine.actions.Actions.PayOut)
        self.assertEqual(1, len(step))

        step = self.mapper._search(engine.actions.Actions.SellShares)
        self.assertEqual(3, len(step))

        step = self.mapper._search(engine.actions.Actions.Pass)
        self.assertEqual(8, len(step))

        step = self.mapper._search(engine.actions.Actions.BuyPrivate)
        self.assertEqual(5, len(step))

        step = self.mapper._search(engine.events.Events.NewPhase)
        self.assertEqual(1, len(step))

    def test__select_from_single(self):
        step = self.mapper._search(engine.actions.Actions.PayOut)
        result = self.mapper._select(step)
        self.assertEqual(result, engine.actions.PayOut)

    def test__select_from_inherited(self):
        step = self.mapper._search(engine.actions.Actions.Pass)
        result = self.mapper._select(step)
        self.assertEqual(result, engine.actions.Pass)

        step = self.mapper._search(engine.actions.Actions.SellShares)
        result = self.mapper._select(step)
        self.assertEqual(result, engine.actions.SellShare)

        step = self.mapper._search(engine.actions.Actions.Skip)
        result = self.mapper._select(step)
        self.assertEqual(result, engine.actions.Skip)

        step = self.mapper._search(engine.actions.Actions.BuyPrivate)
        result = self.mapper._select(step)
        self.assertEqual(result, engine.actions.BuyPrivate)

    def test_run(self):
        step = engine.actions.Actions.Withhold
        result = self.mapper.run(step)
        self.assertEqual(result, engine.actions.Withhold)

    def test_map_type(self):
        name = 'Withhold'
        result = self.mapper.map_type(name)
        self.assertEqual(engine.actions.Actions.Withhold, result)

        name = 'TrainsRust'
        result = self.mapper.map_type(name)
        self.assertEqual(engine.events.Events.TrainsRust, result)

        # This shall throw an error
        with self.assertRaises(KeyError) as e:
            self.mapper.map_type('Unknown')
        self.assertEqual(
            "'No matching engine step found: Unknown'", str(e.exception)
        )
