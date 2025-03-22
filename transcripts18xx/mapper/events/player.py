#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


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
            event='PresidentNomination',
            player=match.group(1),
            company=match.group(2)
        )
    return None


def has_priority_deal(line: str) -> dict | None:
    match = re.search(r'(.*?) has priority deal', line)
    if match:
        return dict(
            event='PriorityDeal',
            player=match.group(1)
        )
    return None


def operates_company(line: str) -> dict | None:
    match = re.search(r'(.*?) operates (.*)', line)
    if match:
        return dict(
            event='CompanyOperation',
            player=match.group(1),
            company=match.group(2)
        )
    return None
