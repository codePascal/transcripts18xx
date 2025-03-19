#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def buy(line: str) -> dict | None:
    if 'share' in line:
        return _buy_share(line)
    if 'train' in line:
        return _buy_train(line)
    else:
        return _buy_private(line)


def _buy_share(line: str) -> dict | None:
    match = re.search(r'(\w+) buys a (\d+)% share of (.*?) from the (.*?) for \$(\d+)', line)
    if match:
        return dict(
            action='Buy',
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3),
            source=match.group(4),
            amount=match.group(5)
        )
    return None


def _buy_train(line: str) -> dict | None:
    match = re.search(r'(\D) buys a (\d+) train for \$(\d+) from (.*)', line)
    if match:
        return dict(
            action='Buy',
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
        match = re.search(r'(\w+) wins the auction for (.*?) with a bid of \$(\d+)', line)
    if match is None:
        # If no other bids present, another log will be printed
        match = re.search(r'(\w+) wins the auction for (.*?) with the only bid of \$(\d+)', line)
    if match:
        return dict(
            action='Buy',
            player=match.group(1),
            private=match.group(2),
            amount=match.group(3)
        )
    return None
