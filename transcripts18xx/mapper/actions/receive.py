#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def receive(line: str) -> dict | None:
    if 'share' in line:
        if 'sell' in line:
            return None
        else:
            return _receive_share(line)
    else:
        return _receive_funds(line)


def _receive_share(line: str) -> dict | None:
    match = re.search(r'(\D) receives a (\d+)% share of (.*)', line)
    if match:
        return dict(
            action='Receive',
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )
    return None


def _receive_funds(line: str) -> dict | None:
    match = re.search(r'(\D) receives \$(\d+)', line)
    if match:
        return dict(
            action='Receive',
            company=match.group(1),
            amount=match.group(2)
        )
    return None
