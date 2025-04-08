#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import pandas as pd

from ..patterns.mapper import PatternProcessor
from . import player, company


class StatesMapper(object):

    def __init__(self, df: pd.DataFrame):
        self._df = df

        players = set([p for p in self._df.player if pd.notna(p)])
        self._players = [player.PlayerState(p) for p in players]

        companies = set([c for c in self._df.company if pd.notna(c)])
        self._companies = [company.CompanyState(c) for c in companies]

    def _player_idx(self, name: str) -> int:
        return [i for i, p in enumerate(self._players) if p.name == name][0]

    def _company_idx(self, name: str) -> int:
        return [i for i, c in enumerate(self._companies) if c.name == name][0]

    def map(self):
        for _, row in self._df.iterrows():
            print(row.type)
            PatternProcessor().run(row.type)
