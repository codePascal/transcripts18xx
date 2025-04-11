#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import unittest
import pandas as pd

from transcripts18xx.engine.steps import step
from transcripts18xx.engine.states import player, company


class BaseStepTest(unittest.TestCase):

    def assertMatch(self, action, line, expected):
        result = action.match(line)
        self.assertEqual(expected, result)


class TestEngineStep(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        class StepEmulator(step.EngineStep):

            def __init__(self):
                super().__init__()

                self.pattern = re.compile(r'(.*?) runs (\d+) tests using (.*)')

            def _process_match(self, line: str, match) -> dict:
                pass

            def process(self, row: pd.Series, players: list[player.PlayerState],
                        companies: list[company.CompanyState]):
                pass

        cls.cls = StepEmulator()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.cls  # remove StepEmulator

    def test__invoke_search(self):
        match = self.cls._invoke_search('Carl runs 10 tests using pytest')
        self.assertIsInstance(match, re.Match)
        self.assertEqual('Carl runs 10 tests using pytest', match.group(0))
        self.assertEqual('Carl', match.group(1))
        self.assertEqual('10', match.group(2))
        self.assertEqual('pytest', match.group(3))

        match = self.cls._invoke_search(
            'Ryan & Carl runs 10 tests using pytest'
        )
        self.assertIsInstance(match, re.Match)
        self.assertEqual('Ryan & Carl', match.group(1))
        self.assertEqual('10', match.group(2))
        self.assertEqual('pytest', match.group(3))

        match = self.cls._invoke_search(
            'Carl runs 10 tests using pytest & unittest'
        )
        self.assertIsInstance(match, re.Match)
        self.assertEqual('Carl', match.group(1))
        self.assertEqual('10', match.group(2))
        self.assertEqual('pytest & unittest', match.group(3))

        match = self.cls._invoke_search('Carl runs no tests using pytest')
        self.assertIsNone(match)

    def test__contains_dismiss_key(self):
        ret = self.cls._contains_dismiss_key('Some line to check')
        self.assertFalse(ret)

        self.cls._dismiss = ['dismiss', 'skip']

        ret = self.cls._contains_dismiss_key('Contains key to dismiss')
        self.assertTrue(ret)

        ret = self.cls._contains_dismiss_key('Contains key to dismiss and skip')
        self.assertTrue(ret)

        ret = self.cls._contains_dismiss_key('Contains key todismiss')
        self.assertFalse(ret)

    def test__contains_required_key(self):
        ret = self.cls._contains_required_key('Some line to check')
        self.assertFalse(ret)

        self.cls._required = ['required', 'wanted']

        ret = self.cls._contains_required_key('Contains required key')
        self.assertTrue(ret)

        ret = self.cls._contains_required_key(
            'Contains required and wanted key')
        self.assertTrue(ret)

        ret = self.cls._contains_required_key('Contains requiredkey')
        self.assertFalse(ret)
