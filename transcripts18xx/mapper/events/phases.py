#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class PhaseEvents(enum.IntEnum):
    NewPhase = 0
    BankBroke = 1
    GameOver = 2
    OperatingRound = 3
    StockRound = 4


def events(line: str) -> list:
    return [
        new_phase(line),
        operating_round(line),
        stock_round(line),
        game_over(line),
        bank_broke(line)
    ]


def new_phase(line: str) -> dict | None:
    # `-- Phase x ...`
    match = re.search(r'-- Phase (\w+) \(', line)
    if match:
        return dict(
            event=PhaseEvents.NewPhase.name,
            phase=match.group(1)
        )
    return None


def bank_broke(line: str) -> dict | None:
    match = re.search(r'-- The bank has broken --', line)
    if match:
        return dict(
            event=PhaseEvents.BankBroke.name,
        )
    return None


def game_over(line: str) -> dict | None:
    match = re.search(r'-- Game over:', line)
    if match:
        return dict(
            event=PhaseEvents.GameOver.name,
        )
    return None


def operating_round(line: str) -> dict | None:
    # `-- Operating Round x.y ...`
    match = re.search(r'-- Operating Round (\d+\.\d+)', line)
    if match:
        return dict(
            event=PhaseEvents.OperatingRound.name,
            round=match.group(1)
        )
    return None


def stock_round(line: str) -> dict | None:
    # `-- Stock Round x.y ...`
    match = re.search(r'-- Stock Round (\d+)', line)
    if match:
        return dict(
            event=PhaseEvents.StockRound.name,
            round=match.group(1)
        )
    return None
