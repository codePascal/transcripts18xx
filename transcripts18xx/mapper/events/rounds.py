#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def phase_change(line: str) -> dict | None:
    # `-- Phase x ...`
    match = re.search(r'-- Phase (\d+)', line)
    if match:
        return dict(
            event='PhaseChange',
            phase=match.group(1)
        )
    return None


def game_over(line: str) -> dict | None:
    match = re.search(r'-- Game over:', line)
    if match:
        return dict(
            event='Game Over',
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
