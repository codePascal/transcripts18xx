#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class MarketActions(enum.IntEnum):
    ReceiveShare = 0
    ReceiveFunds = 1
    BuyShare = 2
    SellShare = 3
    SkipShare = 4
    ParCompany = 5
    PlaceBid = 6


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
    # TODO: market event
    match = re.search(r'(.*?) receives a (\d+)% share of (.*)', line)
    if match:
        return dict(
            action=MarketActions.ReceiveShare.name,
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )
    return None


def receive_funds(line: str) -> dict | None:
    # TODO: company event
    if 'share' in line:
        return None
    match = re.search(r'(.*?) receives \$(\d+)', line)
    if match:
        return dict(
            action=MarketActions.ReceiveFunds.name,
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
            action=MarketActions.BuyShare.name,
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
            action=MarketActions.SellShare.name,
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
            action=MarketActions.SkipShare.name,
            player=match.group(1),
        )
    return None


def decline_buy_shares(line: str) -> dict | None:
    match = re.search(r'(.*?) declines to buy shares', line)
    if match:
        return dict(
            action=MarketActions.SkipShare.name,
            player=match.group(1),
        )
    return None


def par_company(line: str) -> dict | None:
    match = re.search(r'(.*?) pars (.*?) at \$(\d+)', line)
    if match:
        return dict(
            action=MarketActions.ParCompany.name,
            player=match.group(1),
            company=match.group(2),
            amount=match.group(3)
        )
    return None


def bid(line: str) -> dict | None:
    match = re.search(r'(.*?) bids \$(\d+) for (.*)', line)
    if match:
        return dict(
            action=MarketActions.PlaceBid.name,
            player=match.group(1),
            amount=match.group(2),
            private=match.group(3),
        )
    return None
