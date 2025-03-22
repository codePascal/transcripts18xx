#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""selector.py

Module implements a matching algorithm to map implemented game patterns
to their name.
"""
import enum

from . import pattern, g1830


class Games(enum.IntEnum):
    """Games

    IntEnum to describe the implemented games.
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


def select_game(game: Games) -> pattern.GamePattern:
    """Matches the game name to its pattern.

    Args:
        game: The game name to map.

    Returns:
        The game pattern.

    Raises:
        ValueError: If the game pattern for the game is not implemented.
    """
    if game == Games.G1830:
        return g1830.Game1830()
    else:
        raise ValueError('Unknown game: {}'.format(game.name))
