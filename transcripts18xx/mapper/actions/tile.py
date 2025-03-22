#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class TileActions(enum.IntEnum):
    SkipTile = 0
    LayTile = 1
    PassTile = 2


def actions(line: str) -> list:
    return [
        lay_tile(line),
        skip_tile(line),
        pass_tile(line)
    ]


def lay_tile(line: str) -> dict | None:
    if 'spends' in line:
        return _place_tile_for_money(line)
    return _place_tile_for_free(line)


def skip_tile(line: str) -> dict | None:
    match = re.search(r'(.*?) skips lay track', line)
    if match:
        return dict(
            action=TileActions.SkipTile.name,
            company=match.group(1),
        )
    return None


def pass_tile(line: str) -> dict | None:
    match = re.search(r'(.*?) passes lay/upgrade track', line)
    if match:
        return dict(
            action=TileActions.PassTile.name,
            company=match.group(1)
        )
    return None


def _place_tile_for_free(line: str) -> dict | None:
    match = re.search(
        r'(.*?) lays tile #(.*?) with rotation (\d+) on (.*)', line
    )
    if match:
        return dict(
            action=TileActions.LayTile.name,
            company=match.group(1),
            tile=match.group(2),
            rotation=match.group(3),
            location=match.group(4)
        )
    return None


def _place_tile_for_money(line: str) -> dict | None:
    match = re.search(
        r'(.*?) spends \$(\d+) and lays tile #(.*?) with rotation (\d+) on (.*)',
        line
    )
    if match:
        return dict(
            action=TileActions.LayTile.name,
            company=match.group(1),
            amount=match.group(2),
            tile=match.group(3),
            rotation=match.group(4),
            location=match.group(5)
        )
    return None
