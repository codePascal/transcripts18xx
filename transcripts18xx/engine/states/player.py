#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""


class Players(object):

    def __init__(self, names: list[str]):
        self.players = [PlayerState(n) for n in names]


class PlayerState(object):

    def __init__(self, name: str):
        self.name = name

        self.cash = 0
        self.value = 0
        self.liquidity = 0
        self.certs = 0
        self.shares = dict()
        self.privates = list()

    def __str__(self):
        attrs = ', '.join(f'{k}={repr(v)}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    def initialize(self, initial_value: int):
        self.cash = initial_value
        self.value = self.cash
        self.liquidity = self.cash
