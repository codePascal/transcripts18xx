#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class PlayerEvents(enum.IntEnum):
    PresidentNomination = 0
    PriorityDeal = 1
    OperatesCompany = 2


def events(line: str) -> list:
    return [
        becomes_president(line),
        has_priority_deal(line),
        operates_company(line),
    ]


def becomes_president(line: str) -> dict | None:
    match = re.search(r'(.*?) becomes the president of (.*)', line)
    if match:
        return dict(
            event=PlayerEvents.PresidentNomination.name,
            player=match.group(1),
            company=match.group(2)
        )
    return None


def has_priority_deal(line: str) -> dict | None:
    match = re.search(r'(.*?) has priority deal', line)
    if match:
        return dict(
            event=PlayerEvents.PriorityDeal.name,
            player=match.group(1)
        )
    return None


def operates_company(line: str) -> dict | None:
    match = re.search(r'(.*?) operates (.*)', line)
    if match:
        return dict(
            event=PlayerEvents.OperatesCompany.name,
            player=match.group(1),
            company=match.group(2)
        )
    return None
