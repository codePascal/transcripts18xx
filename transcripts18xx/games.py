#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""18xx games

Module implements an abstract class and its subclasses to define a 18xx game.
In a 18xx game there are usually companies that can be started by a player
and privates that can be brought by a player and subsequently sold to a company.
"""
import abc
import enum


class Game18xx(abc.ABC):
    """Game18xx

    Base class to define game steps, i.e. how the lines of a transcript shall
    be parsed. By default, checks all available pattern matcher against the
    line.

    Attributes:
        companies: The companies available in the game.
        privates: The privates and their values.
        trains: The available trains.
        initial_round: The name of the initial round. Most games start with an
            auction round named ISR 1.
        start_capital: The start capital depending on the number of players.
        currency: The currency used in the 18xx game variant.
    """

    def __init__(self):
        self.companies = set()
        self.privates = dict()
        self.trains = set()
        self.initial_round = str()
        self.start_capital = dict()
        self.currency = str()


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
        self.start_capital = {
            2: 1200,
            3: 800,
            4: 600,
            5: 480,
            6: 400
        }
        self.currency = '$'


class Game1889(Game18xx):
    """Game1889

    See Also:
        https://github.com/tobymao/18xx/wiki/1889
    """

    def __init__(self):
        super().__init__()

        self.companies = {
            'AR', 'IR', 'KO', 'KU', 'SR', 'TR', 'UR'
        }
        self.privates = {
            'Takamatsu E-Railroad': 20,
            'Mitsubishi Ferry': 30,
            'Ehime Railway': 40,
            'Sumitomo Mines Railway': 50,
            'Dougo Railway': 60,
            'South Iyo Railway': 80,
            'Uno-Takamatsu Ferry': 150
        }
        self.trains = {'2', '3', '4', '5', '6', 'D'}
        self.initial_round = 'ISR 1'
        self.start_capital = {
            2: 420,
            3: 420,
            4: 420,
            5: 390,
            6: 390
        }
        self.currency = '¥'


class Games(enum.IntEnum):
    """Games

    Enum class to describe the implemented games. Naming convention is an
    uppercase `G` prepended before the actual game name, e.g., `G1830`, `G1882`.
    """
    G1830 = 0
    G1889 = 1

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

    def game(self):
        """Retrieves the game name of the game.

        Returns:
            Stripped `G` from game.
        """
        return self.name[1:]
