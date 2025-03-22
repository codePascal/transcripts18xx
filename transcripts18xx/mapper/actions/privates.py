#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def actions(line: str) -> list:
    return [
        buy_private(line),
        skip_private(line),
        pass_private(line),
        pass_auction(line),
        collect_from_private(line)
    ]


def buy_private(line: str) -> dict | None:
    if 'share' in line:
        return None
    if 'train' in line:
        return None
    if 'from' in line:
        return _buy_private_from_player(line)
    return _buy_private_from_auction(line)


def skip_private(line: str) -> dict | None:
    match = re.search(r'(.*?) skips buy companies', line)
    if match:
        return dict(
            action='PrivateBuySkipped',
            company=match.group(1),
        )
    return None


def pass_private(line: str) -> dict | None:
    match = re.search(r'(.*?) passes buy companies', line)
    if match:
        return dict(
            action='PrivatesPassed',
            company=match.group(1)
        )
    return None


def pass_auction(line: str) -> dict | None:
    match = re.search(r'(.*?) passes on (.*)', line)
    if match:
        return dict(
            action='AuctionPassed',
            player=match.group(1),
            private=match.group(2),
        )
    return None


def collect_from_private(line: str) -> dict | None:
    match = re.search(r'(.*?) collects \$(\d+) from (.*)', line)
    if match:
        return dict(
            action='Collect',
            who=match.group(1),
            amount=match.group(2),
            source=match.group(3),
        )
    return None


def _buy_private_from_player(line: str) -> dict | None:
    # In that case a company buys the private from a player
    match = re.search(r'(.*?) buys (.*?) from (.*?) for \$(\d+)', line)
    if match:
        return dict(
            action='PrivateBought',
            company=match.group(1),
            private=match.group(2),
            player=match.group(3),
            amount=match.group(4)
        )
    return None


def _buy_private_from_auction(line: str) -> dict | None:
    # A player buys the company from the initial round
    match = re.search(r'(.*?) buys (.*?) for \$(\d+)', line)
    if match is None:
        # When others have made a bid
        match = re.search(
            r'(.*?) wins the auction for (.*?) with a bid of \$(\d+)', line
        )
    if match is None:
        # If no other bids present, another log will be printed
        match = re.search(
            r'(.*?) wins the auction for (.*?) with the only bid of \$(\d+)',
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
