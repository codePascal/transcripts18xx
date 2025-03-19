#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def operates(line: str) -> dict | None:
    match = re.search(r'(\D) operates (.*)', line)
    if match:
        return dict(
            event='CompanyOperation',
            player=match.group(1),
            company=match.group(2)
        )
    return None
