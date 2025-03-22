#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class PrivatesEvents(enum.IntEnum):
    AllPrivatesClosed = 0
    PrivateClosed = 1
    PrivateAuctioned = 2


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
            event=PrivatesEvents.AllPrivatesClosed.name
        )
    return None


def closes(line: str) -> dict | None:
    match = re.search(r'(.*?) closes', line)
    if match:
        return dict(
            event=PrivatesEvents.PrivateClosed.name,
            private=match.group(1)
        )
    return None


def is_auctioned(line: str) -> dict | None:
    match = re.search(r'(.*?) goes up for auction', line)
    if match:
        return dict(
            event=PrivatesEvents.PrivateAuctioned.name,
            private=match.group(1)
        )
    return None
