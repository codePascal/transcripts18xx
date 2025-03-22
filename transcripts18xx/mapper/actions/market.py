#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def actions(line: str) -> list:
    return [
        receive_share(line),
        receive_funds(line),
        buy_share(line),
        sell_share(line),
        decline_sell_shares(line),
        decline_buy_shares(line),
        par_company(line),
        bid(line)
    ]


def receive_share(line: str) -> dict | None:
    match = re.search(r'(.*?) receives a (\d+)% share of (.*)', line)
    if match:
        return dict(
            action='ShareReceived',
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )
    return None


def receive_funds(line: str) -> dict | None:
    match = re.search(r'(.*?) receives \$(\d+)', line)
    if match:
        return dict(
            action='FundsReceived',
            company=match.group(1),
            amount=match.group(2)
        )
    return None


def buy_share(line: str) -> dict | None:
    match = re.search(
        r'(.*?) buys a (\d+)% share of (.*?) from the (.*?) for \$(\d+)', line
    )
    if match:
        return dict(
            action='ShareBought',
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3),
            source=match.group(4),
            amount=match.group(5)
        )
    return None


def sell_share(line: str) -> dict | None:
    match = re.search(
        r'(.*?) sells (\d+) shares of (.*?) and receives \$(\d+)', line
    )
    if not match:
        match = re.search(
            r'(.*?) sells a (\d)0% share of (.*?) and receives \$(\d+)', line
        )
    if match:
        # Assume 10 shares per company
        return dict(
            action='ShareSold',
            player=match.group(1),
            percentage='{}{}'.format(match.group(2), '0'),
            company=match.group(3),
            amount=match.group(4)
        )
    return None


def decline_sell_shares(line: str) -> dict | None:
    match = re.search(r'(.*?) declines to sell shares', line)
    if match:
        return dict(
            action='ShareSellSkipped',
            player=match.group(1),
        )
    return None


def decline_buy_shares(line: str) -> dict | None:
    match = re.search(r'(.*?) declines to buy shares', line)
    if match:
        return dict(
            action='ShareBuySkipped',
            player=match.group(1),
        )
    return None


def par_company(line: str) -> dict | None:
    match = re.search(r'(.*?) pars (.*?) at \$(\d+)', line)
    if match:
        return dict(
            action='CompanyPared',
            player=match.group(1),
            company=match.group(2),
            amount=match.group(3)
        )
    return None


def bid(line: str) -> dict | None:
    match = re.search(r'(.*?) bids \$(\d+) for (.*)', line)
    if match:
        return dict(
            action='BidPlaced',
            player=match.group(1),
            amount=match.group(2),
            private=match.group(3),
        )
    return None
