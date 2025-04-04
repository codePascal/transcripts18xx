#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""g1830.py

Module implements the game patterns for the game 1830.

See Also:
    https://github.com/tobymao/18xx/wiki/1830
"""

from .pattern import GamePattern


class Game1830(GamePattern):

    def __init__(self):
        super().__init__()

        # handlers = [cls() for cls in PatternHandler.__subclasses__()]

