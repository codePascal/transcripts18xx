#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class CompanyEvents(enum.IntEnum):
    CompanyFloats = 0
    SelectsHome = 1
    DoesNotRun = 2


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
            event=CompanyEvents.CompanyFloats.name,
            company=match.group(1)
        )
    return None


def choose_home(line: str) -> dict | None:
    match = re.search(r'(.*?) must choose city for token', line)
    if match:
        return dict(
            event=CompanyEvents.SelectsHome.name,
            company=match.group(1)
        )
    return None


def does_not_run(line: str) -> dict | None:
    match = re.search(r'(.*?) does not run', line)
    if match:
        return dict(
            event=CompanyEvents.DoesNotRun.name,
            company=match.group(1)
        )
    return None
