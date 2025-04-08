#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""


class CompanyState(object):

    def __init__(self, name: str):
        self.name = name

        self.ipo = 10
        self.market = 0
        self.trains = None
        self.president = None
        self.cash = 0

    def __str__(self):
        attrs = ', '.join(f'{k}={repr(v)}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'
