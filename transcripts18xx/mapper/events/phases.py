#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def events(line: str) -> list:
    return [
        phase_changed(line),
        operating_round(line),
        stock_round(line),
        game_over(line),
        bank_broke(line)
    ]


def phase_changed(line: str) -> dict | None:
    # `-- Phase x ...`
    match = re.search(r'-- Phase (\w+) \(', line)
    if match:
        return dict(
            event='PhaseChanged',
            phase=match.group(1)
        )
    return None


def bank_broke(line: str) -> dict | None:
    match = re.search(r'-- The bank has broken --', line)
    if match:
        return dict(
            event='BankBroken',
        )
    return None


def game_over(line: str) -> dict | None:
    match = re.search(r'-- Game over:', line)
    if match:
        return dict(
            event='GameOver',
        )
    return None


def operating_round(line: str) -> dict | None:
    # `-- Operating Round x.y ...`
    match = re.search(r'-- Operating Round (\d+\.\d+)', line)
    if match:
        return dict(
            event='OperatingRound',
            round=match.group(1)
        )
    return None


def stock_round(line: str) -> dict | None:
    # `-- Stock Round x.y ...`
    match = re.search(r'-- Stock Round (\d+)', line)
    if match:
        return dict(
            event='StockRound',
            round=match.group(1)
        )
    return None
