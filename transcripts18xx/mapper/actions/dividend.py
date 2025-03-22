#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class DividedActions(enum.IntEnum):
    PayDivided = 0
    WithholdDivided = 1


def actions(line: str) -> list:
    return [
        full_pay(line),
        withhold(line)
    ]


def full_pay(line: str) -> dict | None:
    match = re.search(r'(.*?) pays out \$(\d+) = \$(\d+) per share', line)
    if match:
        return dict(
            action=DividedActions.PayDivided.name,
            company=match.group(1),
            amount=match.group(2),
            per_share=match.group(3)
        )
    return None


def withhold(line: str) -> dict | None:
    match = re.search(r'(.*?) withholds \$(\d+)', line)
    if match:
        return dict(
            action=DividedActions.WithholdDivided.name,
            company=match.group(1),
            amount=match.group(2)
        )
    return None
