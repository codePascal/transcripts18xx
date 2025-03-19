#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def all_close(line: str) -> dict | None:
    match = re.search(r'-- Event: Private companies close', line)
    if match:
        return dict(
            event='PrivatesClose'
        )
    return None


def closes(line: str) -> dict | None:
    match = re.search(r'(\D) closes', line)
    if match:
        return dict(
            event='PrivatesClose',
            private=match.group(1)
        )
    return None


def is_auctioned(line: str) -> dict | None:
    match = re.search(r'(\w+) goes up for auction', line)
    if match:
        return dict(
            event='PrivateAuction',
            private=match.group(1)
        )
    return None
