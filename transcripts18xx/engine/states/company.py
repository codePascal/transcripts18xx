#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""


class Companies(object):

    def __init__(self, names: list[str]):
        self.companies = [CompanyState(n) for n in names]


class CompanyState(object):

    def __init__(self, name: str):
        self.name = name

        self.ipo = 10
        self.market = 0
        self.trains = dict()
        self.president = None
        self.cash = 0

    def __str__(self):
        attrs = ', '.join(f'{k}={repr(v)}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    def initialize(self, available_trains: list):
        self.ipo = 10
