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
    if 'from' in line:
        return _buy_private_from_player(line)
    else:
        return _buy_private_from_auction(line)


def collects(line: str) -> dict | None:
    match = re.search(r'(.*?) collects \$(\d+) from (.*)', line)
    if match:
        return dict(
            action='Collect',
            who=match.group(1),
            amount=match.group(2),
            source=match.group(3),
        )
    return None


def passes(line: str) -> dict | None:
    if 'has no valid actions' in line:
        return _no_valid_actions(line)
    if 'passes buy trains' in line:
        return _pass_trains(line)
    if 'passes lay/upgrade track' in line:
        return _pass_tiles(line)
    if 'passes buy companies' in line:
        return _pass_privates(line)
    if 'passes place a token' in line:
        return _pass_token(line)
    if 'passes on ' in line:
        return _pass_auction(line)
    return _pass(line)


def _receive_share(line: str) -> dict | None:
    match = re.search(r'(.*?) receives a (\d+)% share of (.*)', line)
    if match:
        return dict(
            action='ShareReceived',
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )
    return None


def _receive_funds(line: str) -> dict | None:
    match = re.search(r'(.*?) receives \$(\d+)', line)
    if match:
        return dict(
            action='FundsReceived',
            company=match.group(1),
            amount=match.group(2)
        )
    return None


def _buy_share(line: str) -> dict | None:
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


def _buy_train(line: str) -> dict | None:
    match = re.search(r'(.*?) buys a (\w+) train for \$(\d+) from (.*)', line)
    if match:
        return dict(
            action='TrainBought',
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            source=match.group(4),
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


def _pass_privates(line: str) -> dict | None:
    match = re.search(r'(.*?) passes buy companies', line)
    if match:
        return dict(
            action='PrivatesPassed',
            company=match.group(1)
        )
    return None


def _pass_trains(line: str) -> dict | None:
    match = re.search(r'(.*?) passes buy trains', line)
    if match:
        return dict(
            action='TrainsPassed',
            company=match.group(1)
        )
    return None


def _pass_tiles(line: str) -> dict | None:
    match = re.search(r'(.*?) passes lay/upgrade track', line)
    if match:
        return dict(
            action='TilesPassed',
            company=match.group(1)
        )
    return None


def _pass_token(line: str) -> dict | None:
    match = re.search(r'(.*?) passes place a token', line)
    if match:
        return dict(
            action='TokenPassed',
            company=match.group(1)
        )
    return None


def _no_valid_actions(line: str) -> dict | None:
    match = re.search(r'(.*?) has no valid actions and passes', line)
    if match:
        return dict(
            action='Passed',
            player=match.group(1)
        )
    return None


def _pass_auction(line: str) -> dict | None:
    match = re.search(r'(.*?) passes on (.*)', line)
    if match:
        return dict(
            action='AuctionPassed',
            player=match.group(1),
            private=match.group(2),
        )
    return None


def _pass(line: str) -> dict | None:
    match = re.search(r'(.*?) passes', line)
    if match:
        return dict(
            action='Passed',
            player=match.group(1)
        )
    return None
