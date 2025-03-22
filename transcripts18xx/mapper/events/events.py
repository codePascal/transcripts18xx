#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum

from . import company
from . import market
from . import phases
from . import player
from . import privates
from . import trains


class GameEvents(enum.Enum):
    Company = company.CompanyEvents
    Market = market.MarketEvents
    Phases = phases.PhaseEvents
    Player = player.PlayerEvents
    Privates = privates.PrivatesEvents
    Train = trains.TrainEvents


def events(line: str) -> list:
    ret = list()
    ret.extend(company.events(line))
    ret.extend(market.events(line))
    ret.extend(player.events(line))
    ret.extend(privates.events(line))
    ret.extend(phases.events(line))
    ret.extend(trains.events(line))
    return ret
