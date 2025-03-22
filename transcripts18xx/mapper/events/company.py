#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def events(line: str) -> list:
    return [
        floats(line),
        choose_home(line),
        does_not_run(line)
    ]


def floats(line: str) -> dict | None:
    match = re.search(r'(.*?) floats', line)
    if match:
        return dict(
            event='CompanyFloating',
            company=match.group(1)
        )
    return None


def choose_home(line: str) -> dict | None:
    match = re.search(r'(.*?) must choose city for token', line)
    if match:
        return dict(
            event='SelectHome',
            company=match.group(1)
        )
    return None


def does_not_run(line: str) -> dict | None:
    match = re.search(r'(.*?) does not run', line)
    if match:
        return dict(
            event='DoesNotRun',
            company=match.group(1)
        )
    return None
