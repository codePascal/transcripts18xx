#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def floats(line: str) -> dict | None:
    match = re.search(r'(\D) floats', line)
    if match:
        return dict(
            event='CompanyFloating',
            player=match.group(1)
        )
    return None
