#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def close(line: str) -> dict | None:
    match = re.search(r'-- Event: Private companies close', line)
    if match:
        return dict(
            event='PrivatesClose'
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
