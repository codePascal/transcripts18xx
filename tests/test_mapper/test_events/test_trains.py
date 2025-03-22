#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.events import trains


class TestTrainEvents(unittest.TestCase):

    def test_rust(self):
        line = '-- Event: 2 trains rust ( B&O x1, NYC x1, C&O x2, PRR x2) --'
        expected = {
            'event': 'TrainRust',
            'train': '2'
        }
        self.assertEqual(expected, trains.rust(line))
