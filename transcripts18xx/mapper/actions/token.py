#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def actions(line: str) -> list:
    return [
        place_token(line),
        skip_token(line),
        pass_token(line)
    ]


def place_token(line: str) -> dict | None:
    if 'for' in line:
        return _place_token_for_money(line)
    return _place_token_for_free(line)


def skip_token(line: str) -> dict | None:
    match = re.search(r'(.*?) skips place a token', line)
    if match:
        return dict(
            action='TokenSkipped',
            company=match.group(1)
        )
    return None


def pass_token(line: str) -> dict | None:
    match = re.search(r'(.*?) passes place a token', line)
    if match:
        return dict(
            action='TokenPassed',
            company=match.group(1)
        )
    return None


def _place_token_for_free(line: str) -> dict | None:
    match = re.search(r'(.*?) places a token on (.*)', line)
    if match:
        return dict(
            action='TokenPlaced',
            company=match.group(1),
            location=match.group(2)
        )
    return None


def _place_token_for_money(line: str) -> dict | None:
    match = re.search(r'(.*?) places a token on (.*) for \$(\d+)', line)
    if match:
        return dict(
            action='TokenPlaced',
            company=match.group(1),
            location=match.group(2),
            amount=match.group(3)
        )
    return None
