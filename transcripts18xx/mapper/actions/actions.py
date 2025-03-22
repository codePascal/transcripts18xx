#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import dividend
from . import market
from . import passed
from . import privates
from . import tile
from . import token
from . import train


def actions(line: str) -> list:
    ret = list()
    ret.extend(dividend.actions(line))
    ret.extend(market.actions(line))
    ret.extend(passed.actions(line))
    ret.extend(privates.actions(line))
    ret.extend(tile.actions(line))
    ret.extend(token.actions(line))
    ret.extend(train.actions(line))
    return ret
