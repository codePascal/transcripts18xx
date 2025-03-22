#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""g1830.py

Module implements the game patterns for the game 1830.

See Also:
    https://github.com/tobymao/18xx/wiki/1830
"""

from ..mapper.actions import actions
from ..mapper.events import events
from .pattern import GamePattern


class Game1830(GamePattern):

    def __init__(self):
        super().__init__()

    def _check_events(self, line: str) -> dict | None:
        return self._match(events.events(line))

    def _check_actions(self, line: str) -> dict | None:
        return self._match(actions.actions(line))

    def extract_pattern(self, line: str) -> dict | None:
        return self._match(
            [
                self._check_events(line),
                self._check_actions(line)
            ]
        )
