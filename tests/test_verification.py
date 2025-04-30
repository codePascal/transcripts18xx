#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import unittest.mock

from transcripts18xx import verification


class TestStateVerification(unittest.TestCase):

    def test__compare_nested_dicts_no_diff(self):
        d1 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        ret = st._compare_nested_dicts(d1, d2)
        self.assertFalse(ret)

    def test__compare_nested_dicts_diff(self):
        d1 = dict(x=10, y='some other', z=dict(a=2, b=3, c=['abc']))
        d2 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        ret = st._compare_nested_dicts(d1, d2)
        self.assertEqual(
            {'z.a': (2, 1), 'y': ('some other', 'some string')}, ret
        )

    def test__compare_nested_dicts_missing_left(self):
        d1 = dict(x=10, z=dict(a=1, b=3, c=['abc']))
        d2 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        ret = st._compare_nested_dicts(d1, d2)
        self.assertEqual({'y': ('<missing>', 'some string')}, ret)

    def test__compare_nested_dicts_missing_right(self):
        d1 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(y='some string', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        ret = st._compare_nested_dicts(d1, d2)
        self.assertEqual({'x': (10, '<missing>')}, ret)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__display_differences(self, mock_stdout):
        d1 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(y='some other', z=dict(a=1, c=['xyz']))

        st = verification.StateVerification()
        diffs = st._compare_nested_dicts(d1, d2)
        diffs = dict(sorted(diffs.items()))  # sort for reproducibility

        expected = str(
            "===================================\n"
            "State Differences: Parsed vs. Truth\n"
            "-----------------------------------\n"
            "x: 10 != '<missing>'\n"
            "y: 'some string' != 'some other'\n"
            "z.b: 3 != '<missing>'\n"
            "z.c: ['abc'] != ['xyz']\n"
            "-----------------------------------\n"
        )
        st._display_differences(diffs)
        self.assertEqual(expected, mock_stdout.getvalue())

    def test__evaluate_differences_mismatch(self):
        d1 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(x=10, y='some other', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        diffs = st._compare_nested_dicts(d1, d2)
        ret = st._evaluate_differences(diffs)
        self.assertFalse(ret)

    def test__evaluate_differences_match(self):
        d1 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        diffs = st._compare_nested_dicts(d1, d2)
        ret = st._evaluate_differences(diffs)
        self.assertTrue(ret)

    def test__evaluate_differences_missing_left(self):
        d1 = dict(y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        diffs = st._compare_nested_dicts(d1, d2)
        ret = st._evaluate_differences(diffs)
        self.assertTrue(ret)

    def test__evaluate_differences_missing_right(self):
        d1 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(x=10, z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        diffs = st._compare_nested_dicts(d1, d2)
        ret = st._evaluate_differences(diffs)
        self.assertFalse(ret)

    def test_run(self):
        d1 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))
        d2 = dict(x=10, y='some string', z=dict(a=1, b=3, c=['abc']))

        st = verification.StateVerification()
        ret = st.run(d1, d2)
        self.assertTrue(ret)
