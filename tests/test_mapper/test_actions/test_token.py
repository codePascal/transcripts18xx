#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import token


class TestTokenActions(unittest.TestCase):

    def test_place_token(self):
        line = 'B&O places a token on F16 (Scranton)'
        expected = {
            'action': token.TokenActions.PlaceToken.name,
            'company': 'B&O',
            'location': 'F16 (Scranton)'
        }
        self.assertEqual(expected, token.place_token(line))

        line = 'B&O places a token on F16 (Scranton) for $40'
        expected = {
            'action': token.TokenActions.PlaceToken.name,
            'company': 'B&O',
            'location': 'F16 (Scranton)',
            'amount': '40'
        }
        self.assertEqual(expected, token.place_token(line))

    def test_skip_token(self):
        line = 'B&O skips place a token'
        expected = {
            'action': token.TokenActions.SkipToken.name,
            'company': 'B&O',
        }
        self.assertEqual(expected, token.skip_token(line))

    def test_pass_token(self):
        line = 'B&O passes place a token'
        expected = {
            'action': token.TokenActions.PassToken.name,
            'company': 'B&O'
        }
        self.assertEqual(expected, token.pass_token(line))
