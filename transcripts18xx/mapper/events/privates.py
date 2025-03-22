#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def events(line: str) -> list:
    return [
        all_close(line),
        closes(line),
        is_auctioned(line)
    ]


def all_close(line: str) -> dict | None:
    match = re.search(r'-- Event: Private companies close', line)
    if match:
        return dict(
            event='AllPrivatesClose'
        )
    return None


def closes(line: str) -> dict | None:
    match = re.search(r'(.*?) closes', line)
    if match:
        return dict(
            event='PrivateCloses',
            private=match.group(1)
        )
    return None


def is_auctioned(line: str) -> dict | None:
    match = re.search(r'(.*?) goes up for auction', line)
    if match:
        return dict(
            event='PrivateAuction',
            private=match.group(1)
        )
    return None
