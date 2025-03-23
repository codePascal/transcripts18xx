#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""


class PlayerState(object):

    def __init__(self, name: str):
        self.name = name

        self.cash = 600  # 1830 - 4 player game; split $2400
        self.value = 600
        self.liquidity = 600
        self.certs = 0
        self.shares = 0
        self.privates = None

    def __str__(self):
        attrs = ', '.join(f'{k}={repr(v)}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    # TODO: implement some logic to process lines here?