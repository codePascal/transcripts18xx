#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import common, company, player


def actions(line: str) -> list:
    ret = list()
    ret.extend(common.actions(line))
    ret.extend(company.actions(line))
    ret.extend(player.actions(line))
    return ret
