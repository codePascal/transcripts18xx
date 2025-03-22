#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def events(line: str) -> list:
    return [
        share_price_moves(line)
    ]


def share_price_moves(line: str) -> dict | None:
    match = re.search(
        r"(.*?)'s share price moves (.*?) from \$(\d+) to \$(\d+)", line
    )
    if match:
        return dict(
            event='SharePriceMove',
            company=match.group(1),
            direction=match.group(2),
            share_price=match.group(4)
        )
    return None
