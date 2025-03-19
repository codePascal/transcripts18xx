#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import privates, trains, rounds, player, company, market


def events(line: str) -> list:
    return [
        company_events(line)
        + market_events(line)
        + player_events(line)
        + private_events(line)
        + round_events(line)
        + train_events(line)
    ]


def company_events(line: str) -> list:
    pass


def market_events(line: str) -> list:
    pass


def player_events(line: str) -> list:
    pass


def private_events(line: str) -> list:
    pass


def round_events(line: str) -> list:
    pass


def train_events(line: str) -> list:
    pass
