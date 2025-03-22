#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.mapper.actions import tile


class TestTileActions(unittest.TestCase):

    def test_lay_tile(self):
        line = 'B&O lays tile #7 with rotation 1 on I17'
        expected = {
            'action': tile.TileActions.LayTile.name,
            'company': 'B&O',
            'tile': '7',
            'rotation': '1',
            'location': 'I17'
        }
        self.assertEqual(expected, tile.lay_tile(line))

        line = 'B&O (HO) spends $80 and lays tile #7 with rotation 1 on I17'
        expected = {
            'action': tile.TileActions.LayTile.name,
            'company': 'B&O',
            'amount': '80',
            'tile': '7',
            'rotation': '1',
            'location': 'I17'
        }
        self.assertEqual(expected, tile.lay_tile(line))

    def test_skip_tile(self):
        line = 'B&O skips lay track'
        expected = {
            'action': tile.TileActions.SkipTile.name,
            'company': 'B&O'
        }
        self.assertEqual(expected, tile.skip_tile(line))

    def test_pass_tile(self):
        line = 'B&O passes lay/upgrade track'
        expected = {
            'action': tile.TileActions.PassTile.name,
            'company': 'B&O'
        }
        self.assertEqual(expected, tile.pass_tile(line))
