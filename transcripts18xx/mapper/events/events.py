#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import privates, trains, phases, player, company, market


def events(line: str) -> list:
    ret = list()
    ret.extend(company.events(line))
    ret.extend(market.events(line))
    ret.extend(player.events(line))
    ret.extend(privates.events(line))
    ret.extend(phases.events(line))
    ret.extend(trains.events(line))
    return ret
