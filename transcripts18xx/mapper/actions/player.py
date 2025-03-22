#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def actions(line: str) -> list:
    return [
        bids(line),
        operates_company(line),
        pars_company(line),
        declines_sell_shares(line),
        sells_shares(line),
        declines_buy_shares(line),
        contributes_for_train(line)
    ]


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


def declines_buy_shares(line: str) -> dict | None:
    match = re.search(r'(\D) declines to buy shares', line)
    if match:
        return dict(
            action='BuySharesSkipped',
            player=match.group(1),
        )
    return None


def sells_shares(line: str) -> dict | None:
    match = re.search(
        r'(\D) sells (\d+) shares of (.*?) and receives \$(\d+)', line
    )
    if not match:
        match = re.search(
            r'(\D) sells a (\d)0% share of (.*?) and receives \$(\d+)', line
        )
    if match:
        return dict(
            action='SharesSold',
            player=match.group(1),
            num_shares=match.group(2),
            company=match.group(3),
            amount=match.group(4)
        )
    return None


def contributes_for_train(line: str) -> dict | None:
    match = re.search(r'(\D) contributes \$(\d+)', line)
    if match:
        return dict(
            action='TrainBuyContributed',
            player=match.group(1),
            amount=match.group(2)
        )
    return None
