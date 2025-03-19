#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def bid(line: str) -> dict | None:
    match = re.search(r'(\w+) bids \$(\d+) for (.*)', line)
    if match:
        return dict(
            action='Bid',
            player=match.group(1),
            amount=match.group(2),
            private=match.group(3),
        )
    return None
