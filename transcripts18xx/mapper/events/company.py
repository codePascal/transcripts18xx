#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def events(line: str) -> list:
    return [
        floats(line),
        choose_home(line)
    ]


def floats(line: str) -> dict | None:
    match = re.search(r'(\w+) floats', line)
    if match:
        return dict(
            event='CompanyFloating',
            player=match.group(1)
        )
    return None


def choose_home(line: str) -> dict | None:
    match = re.search(r'(\w+) must choose city for token', line)
    if match:
        return dict(
            event='SelectHome',
            company=match.group(1)
        )
    return None
