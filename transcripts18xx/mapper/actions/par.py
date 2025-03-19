#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def par(line: str) -> dict | None:
    match = re.search(r'(\w+) pars (.*?) at \$(\d+)', line)
    if match:
        return dict(
            action='Par',
            player=match.group(1),
            company=match.group(2),
            amount=match.group(3)
        )
    return None
