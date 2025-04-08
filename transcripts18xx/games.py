#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""18xx games

Module implements an abstract class to define, search and process game steps.
"""
import abc
import enum

import pandas as pd

from .engine.engine import LineParser


class Game18xx(abc.ABC):
    """Game18xx

    Base class to define game steps, i.e. how the lines of a transcript shall
    be parsed. By default, checks all available pattern matcher against the
    line.

    Attributes:

    """

    def __init__(self):
        self.pre_processor = LineParser()

        self.companies = set()
        self.privates = dict()
        self.trains = set()
        self.initial_round = str()
        self.start_capital = int()

    def extract_pattern(self, line: str) -> dict | None:
        """Parses the line and checks for matches in the given recipes.

        Args:
            line: A transcript line to parse.

        Returns:
            If a match is found, returns the result parsed in a dictionary.
            Otherwise, returns None.
        """
        return self.pre_processor.run(line)

    def post_process_step(self, row: pd.DataFrame) -> None:
        pass


class Game1830(Game18xx):
    """Game1830

    See Also:
        https://github.com/tobymao/18xx/wiki/1830
    """

    def __init__(self):
        super().__init__()

        self.companies = {
            'B&M', 'B&O', 'C&O', 'CPR', 'ERIE', 'NYC', 'NYNH', 'PRR'
        }
        self.privates = {
            'Baltimore & Ohio': 220,
            'Champlain & St.Lawrence': 40,
            'Mohawk & Hudson': 110,
            'Delaware & Hudson': 70,
            'Camden & Amboy': 160,
            'Schuylkill Valley': 20
        }
        self.trains = {'2', '3', '4', '5', '6', 'D'}
        self.initial_round = 'ISR 1'
        self.start_capital = 2400


class Games(enum.IntEnum):
    """Games

    Class to describe the implemented games.
    """
    G1830 = 0

    def __str__(self) -> str:
        # Return name for usage in argparse
        return self.name

    @staticmethod
    def argparse(game: str):
        """Maps the game name to its enum member.

        Args:
            game: The enum member name as string.

        Returns:
            The enum member matching to the string.

        Raises:
            ValueError: If game is not found in the enum.
        """
        try:
            return Games[game]
        except KeyError:
            raise ValueError()

    def select(self) -> Game18xx:
        """Matches the game to its struct.

        Returns:
            The game.

        Raises:
            ValueError: If the game is not implemented.
        """
        if self == Games.G1830:
            return Game1830()
        else:
            raise ValueError('Unknown game: {}'.format(self.name))
