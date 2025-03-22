#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.events import company


class TestCompanyEvents(unittest.TestCase):

    def test_floats(self):
        line = 'B&O floats'
        expected = {
            'event': 'CompanyFloating',
            'company': 'B&O'
        }
        self.assertEqual(expected, company.floats(line))

    def test_choose_home(self):
        line = 'B&O must choose city for token'
        expected = {
            'event': 'SelectHome',
            'company': 'B&O'
        }
        self.assertEqual(expected, company.choose_home(line))

    def test_does_not_run(self):
        line = 'B&O does not run'
        expected = {
            'event': 'DoesNotRun',
            'company': 'B&O',
        }
        self.assertEqual(expected, company.does_not_run(line))
