#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class TokenActions(enum.IntEnum):
    SkipToken = 0
    PlaceToken = 1
    PassToken = 2


def actions(line: str) -> list:
    return [
        place_token(line),
        skip_token(line),
        pass_token(line)
    ]


def place_token(line: str) -> dict | None:
    if 'for' in line:
        ret = _place_token_for_money(line)
    else:
        ret = _place_token_for_free(line)
    if ret:
        if '(' in ret['company']:
            # If a company uses a private it is recorded as e.g. `B&O (MH) ...`
            ret['company'] = ret['company'].split('(')[0].strip()
    return ret


def skip_token(line: str) -> dict | None:
    match = re.search(r'(.*?) skips place a token', line)
    if match:
        return dict(
            action=TokenActions.SkipToken.name,
            company=match.group(1)
        )
    return None


def pass_token(line: str) -> dict | None:
    match = re.search(r'(.*?) passes place a token', line)
    if match:
        return dict(
            action=TokenActions.PassToken.name,
            company=match.group(1)
        )
    return None


def _place_token_for_free(line: str) -> dict | None:
    match = re.search(r'(.*?) places a token on (.*)', line)
    if match:
        return dict(
            action=TokenActions.PlaceToken.name,
            company=match.group(1),
            location=match.group(2)
        )
    return None


def _place_token_for_money(line: str) -> dict | None:
    match = re.search(r'(.*?) places a token on (.*) for \$(\d+)', line)
    if match:
        return dict(
            action=TokenActions.PlaceToken.name,
            company=match.group(1),
            location=match.group(2),
            amount=match.group(3)
        )
    return None
