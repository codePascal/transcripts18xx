#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def actions(line: str) -> list:
    return [
        places_token(line),
        skips_token(line),
        lays_tile(line),
        skips_tile(line),
        runs_train(line),
        skips_run_train(line),
        skips_buy_private(line),
        pays_dividend(line),
        skips_buy_train(line),
        withholds(line),
        discards_train(line),
        exchanges_train(line)
    ]


def places_token(line: str) -> dict | None:
    match = re.search(r'(.*?) places a token on (.*)', line)
    if match:
        return dict(
            action='TokenPlaced',
            company=match.group(1),
            location=match.group(2)
        )
    return None


def lays_tile(line: str) -> dict | None:
    match = re.search(
        r'(.*?) spends \$(\d+) and lays tile #(.*?) with rotation (\d+) on (.*)',
        line
    )
    if match:
        return dict(
            action='TilePlaced',
            company=match.group(1),
            amount=match.group(2),
            tile=match.group(3),
            rotation=match.group(4),
            location=match.group(5)
        )
    else:
        match = re.search(
            r'(.*?) lays tile #(.*?) with rotation (\d+) on (.*)', line
        )
        if match:
            return dict(
                action='TilePlaced',
                company=match.group(1),
                tile=match.group(2),
                rotation=match.group(3),
                location=match.group(4)
            )
    return None


def runs_train(line: str) -> dict | None:
    match = re.search(r'(.*?) runs a (\w) train for \$(\d+): (.*)', line)
    if match:
        return dict(
            action='TrainRan',
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            route=match.group(4)
        )
    return None


def pays_dividend(line: str) -> dict | None:
    match = re.search(r'(.*?) pays out \$(\d+) = \$(\d+) per share', line)
    if match:
        return dict(
            action='DividendPayed',
            company=match.group(1),
            amount=match.group(2),
            per_share=match.group(3)
        )
    return None


def withholds(line: str) -> dict | None:
    match = re.search(r'(.*?) withholds \$(\d+)', line)
    if match:
        return dict(
            action='DividendWithheld',
            company=match.group(1),
            amount=match.group(2)
        )
    return None


def skips_token(line: str) -> dict | None:
    match = re.search(r'(.*?) skips place a token', line)
    if match:
        return dict(
            action='TokenSkipped',
            company=match.group(1)
        )
    return None


def skips_tile(line: str) -> dict | None:
    match = re.search(r'(.*?) skips lay track', line)
    if match:
        return dict(
            action='TileSkipped',
            company=match.group(1),
        )
    return None


def skips_run_train(line: str) -> dict | None:
    match = re.search(r'(.*?) skips run routes', line)
    if match:
        return dict(
            action='TrainRunSkipped',
            company=match.group(1),
        )
    return None


def skips_buy_private(line: str) -> dict | None:
    match = re.search(r'(.*?) skips buy companies', line)
    if match:
        return dict(
            action='PrivateBuySkipped',
            company=match.group(1),
        )
    return None


def skips_buy_train(line: str) -> dict | None:
    match = re.search(r'(.*?) skips buy trains', line)
    if match:
        return dict(
            action='TrainBuySkipped',
            company=match.group(1),
        )
    return None


def discards_train(line: str) -> dict | None:
    match = re.search(r'(.*?) discards (\w+)', line)
    if match:
        return dict(
            action='TrainDiscarded',
            company=match.group(1),
            train=match.group(2)
        )
    return None


def exchanges_train(line: str) -> dict | None:
    match = re.search(
        r'(.*?) exchanges a (\d+) for a (\D) train for \$(\d+) from (.*)',
        line
    )
    if match:
        return dict(
            action='TrainExchanged',
            company=match.group(1),
            old_train=match.group(2),
            new_train=match.group(3),
            amount=match.group(4),
            source=match.group(5)
        )
    return None
