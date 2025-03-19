#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def passes(line: str) -> dict | None:
    match = re.search(r'(\w+) passes', line)
    if match:
        return dict(
            event='Pass',
            who=match.group(1)
        )
    return None