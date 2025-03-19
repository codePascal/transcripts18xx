# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def collect(line: str) -> dict | None:
    match = re.search(r'(\w+) collects \$(\d+) from (.*)', line)
    if match:
        return dict(
            action='Collect',
            player=match.group(1),
            amount=match.group(2),
            source=match.group(3),
        )
    return None
