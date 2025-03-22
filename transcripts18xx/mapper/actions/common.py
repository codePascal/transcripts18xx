#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def actions(line: str) -> list:
    return [
        receives(line),
        buys(line),
        collects(line),
        passes(line)
    ]


def receives(line: str) -> dict | None:
    if 'share' in line:
        if 'sell' in line:
            return None
        else:
            return _receive_share(line)
    else:
        return _receive_funds(line)


def buys(line: str) -> dict | None:
    if 'share' in line:
        return _buy_share(line)
    if 'train' in line:
        return _buy_train(line)
    else:
        return _buy_private(line)


def collects(line: str) -> dict | None:
    match = re.search(r'(\D) collects \$(\d+) from (.*)', line)
    if match:
        return dict(
            action='Collect',
            who=match.group(1),
            amount=match.group(2),
            source=match.group(3),
        )
    return None


def passes(line: str) -> dict | None:
    match = re.search(r'(\w+) passes', line)
    if match:
        return dict(
            action='Passed',
            who=match.group(1)
        )
    return None


def _receive_share(line: str) -> dict | None:
    match = re.search(r'(\D) receives a (\d+)% share of (.*)', line)
    if match:
        return dict(
            action='ShareReceived',
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )
    return None


def _receive_funds(line: str) -> dict | None:
    match = re.search(r'(\D) receives \$(\d+)', line)
    if match:
        return dict(
            action='FundsReceived',
            company=match.group(1),
            amount=match.group(2)
        )
    return None


def _buy_share(line: str) -> dict | None:
    match = re.search(
        r'(\D) buys a (\d+)% share of (.*?) from the (.*?) for \$(\d+)', line
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


def _buy_train(line: str) -> dict | None:
    match = re.search(r'(\D) buys a (\w+) train for \$(\d+) from (.*)', line)
    if match:
        return dict(
            action='TrainBought',
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            source=match.group(4),
        )
    return None


def _buy_private(line: str) -> dict | None:
    match = re.search(r'(\w+) buys (.*?) for \$(\d+)', line)
    if match is None:
        # When others have made a bid
        match = re.search(
            r'(\w+) wins the auction for (.*?) with a bid of \$(\d+)', line
        )
    if match is None:
        # If no other bids present, another log will be printed
        match = re.search(
            r'(\w+) wins the auction for (.*?) with the only bid of \$(\d+)',
            line
        )
    if match:
        return dict(
            action='PrivateBought',
            player=match.group(1),
            private=match.group(2),
            amount=match.group(3)
        )
    return None
