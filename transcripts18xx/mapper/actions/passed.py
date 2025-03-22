#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def actions(line: str) -> list:
    return [
        no_valid_actions(line),
        regular_pass(line)
    ]


def no_valid_actions(line: str) -> dict | None:
    match = re.search(r'(.*?) has no valid actions and passes', line)
    if match:
        return dict(
            action='Passed',
            player=match.group(1)
        )
    return None


def regular_pass(line: str) -> dict | None:
    match = line.split()
    if len(match) == 2 and match[1] == 'passes':
        return dict(
            action='Passed',
            player=match[0]
        )
    return None
