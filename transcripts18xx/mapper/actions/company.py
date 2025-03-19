#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def places_token(line: str) -> dict | None:
    match = re.search(r'(\D) places a token on (.*)', line)
    if match:
        return dict(
            action='TokenPlaced',
            company=match.group(1),
            location=match.group(2)
        )
    return None


def lays_tile(line: str) -> dict | None:
    match = re.search(r'(\D) lays tile #(.*?) with rotation (\d+) on (.*)', line)
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
    match = re.search(r'(\D) runs a (\d+) train for \$(\d+): (.*)', line)
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
    match = re.search(r'(\D) pays out \$(\d+) = \$(\d+) per share', line)
    if match:
        return dict(
            action='DividendPayed',
            company=match.group(1),
            amount=match.group(2),
            per_share=match.group(3)
        )
    return None


def skips_token(line: str) -> dict | None:
    match = re.search(r'(\D) skips place a token', line)
    if match:
        return dict(
            action='TokenSkipped',
            company=match.group(1)
        )
    return None


def skips_tile(line: str) -> dict | None:
    match = re.search(r'(\D) skips place tile', line)
    if match:
        return dict(
            action='TileSkipped',
            company=match.group(1),
        )
    return None


def skips_run_train(line: str) -> dict | None:
    match = re.search(r'(\D) skips run routes', line)
    if match:
        return dict(
            action='TrainSkipped',
            company=match.group(1),
        )
    return None


def skips_buy_private(line: str) -> dict | None:
    match = re.search(r'(\D) skips buy companies', line)
    if match:
        return dict(
            action='PrivateBuySkipped',
            company=match.group(1),
        )
    return None
