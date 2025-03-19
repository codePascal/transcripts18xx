#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def rust(line: str) -> dict | None:
    match = re.search(r'-- Event: (\d+) trains rust', line)
    if match:
        return dict(
            event='TrainRust',
            train=match.group(1)
        )
    return None
