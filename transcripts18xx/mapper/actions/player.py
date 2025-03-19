#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def bids(line: str) -> dict | None:
    match = re.search(r'(\w+) bids \$(\d+) for (.*)', line)
    if match:
        return dict(
            action='BidPlaced',
            player=match.group(1),
            amount=match.group(2),
            private=match.group(3),
        )
    return None


def operates_company(line: str) -> dict | None:
    match = re.search(r'(\D) operates (.*)', line)
    if match:
        return dict(
            event='CompanyOperated',
            player=match.group(1),
            company=match.group(2)
        )
    return None


def pars_company(line: str) -> dict | None:
    match = re.search(r'(\w+) pars (.*?) at \$(\d+)', line)
    if match:
        return dict(
            action='CompanyPared',
            player=match.group(1),
            company=match.group(2),
            amount=match.group(3)
        )
    return None


def declines_sell_shares(line: str) -> dict | None:
    match = re.search(r'(\D) declines to sell shares', line)
    if match:
        return dict(
            action='SellSharesSkipped',
            player=match.group(1),
        )
    return None
