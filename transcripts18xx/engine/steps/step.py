#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic step matching and processing

Module implements abstract base class to match a pattern to a string and
run some post-processing on the line if a match was found.
"""
import abc
import enum
import pandas as pd
import re

from typing import Type

from ..states.player import Players
from ..states.company import Companies


class StepType(enum.IntEnum):
    """StepType

    Enum class to describe a step by a type. The members below depict the
    different actions that are available and events that occur during the game.
    """
    PayOut = 0
    Withhold = 1
    BuyShare = 2
    SellShares = 3
    Par = 5
    Bid = 6
    Pass = 7
    Skip = 8
    Collect = 9
    BuyPrivate = 10
    LayTile = 11
    PlaceToken = 12
    BuyTrain = 13
    RunTrain = 14
    DiscardTrain = 15
    ExchangeTrain = 16
    Contribute = 17
    ReceiveShare = 18
    ReceiveFunds = 19
    CompanyFloats = 20
    SelectsHome = 21
    DoesNotRun = 22
    SharePriceMoves = 23
    NewPhase = 24
    BankBroke = 25
    GameOver = 26
    OperatingRound = 27
    StockRound = 28
    PresidentNomination = 29
    PriorityDeal = 30
    OperatesCompany = 31
    AllPrivatesClose = 32
    PrivateCloses = 33
    PrivateAuctioned = 34
    TrainsRust = 35
    PlayerGoesBankrupt = 36
    GameEndedManually = 37


class StepParent(enum.IntEnum):
    """StepParent

    Enum class to describe a group of steps. 18xx games have actions a player or
    a company can take and events that are a result from actions taken or timing
    related.
    """
    Event = 0
    Action = 1


class EngineStep(abc.ABC):
    """EngineStep

    Class to map a line to a pattern. Each subclass implements a pattern, that
    is compared to a line. The pattern is implemented as a regular expression.
    Further, the subclasses implement the post-processing of this match.
    Each step implements a rule on how to update the game state w.r.t. the
    whole game environment.

    Attributes:
        pattern: The expression that shall be matched to the line.
        type: The type of the pattern, see `StepType`.
        parent: The pattern group the pattern is part of, see `StepParent`.
        _dismiss: Keywords that result in the line being ignored if they exist
            in the line.
        _required: Keywords that need to be found in the line. Otherwise, the
            line is ignored. If multiple keywords are given, only one must be
            found for the line to be checked.
    """

    def __init__(self):
        self.pattern = None
        self.type = Type[StepType]
        self.parent = Type[StepParent]

        self._dismiss = list()
        self._required = list()

    def _invoke_search(self, line: str) -> re.Match | None:
        # Invokes the search command.
        if self.pattern is None:
            return None
        return self.pattern.search(line)

    @abc.abstractmethod
    def _process_match(self, line: str, match) -> dict:
        # Processes the match.
        pass

    def _contains_dismiss_key(self, line: str) -> bool:
        # Checks if key to dismiss exists in line as single word.
        return any(key in line.split() for key in self._dismiss)

    def _contains_required_key(self, line: str) -> bool:
        # Checks if required key exists in line as single word.
        return any(key in line.split() for key in self._required)

    def _search(self, line: str) -> re.Match | None:
        # Maps the pattern to the line.
        if self._contains_dismiss_key(line):
            return None
        if not self._required or self._contains_required_key(line):
            return self._invoke_search(line)
        return None

    def _process(self, line: str, match) -> dict:
        # Processes the match and adds general information.
        ret = self._process_match(line, match)
        ret['type'] = self.type.name
        ret['parent'] = self.parent.name
        return ret

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        # Invoke the engine step to update game state accordingly.
        pass

    def match(self, line: str) -> dict | None:
        """Matches and processes a line to the pattern.

        Args:
            line: The line to compare to the pattern.

        Returns:
            A dictionary with the matches processed, or None if no match found.
        """
        match = self._search(line)
        if match:
            return self._process(line, match)
        return None

    def state_update(self, row: pd.Series, players: Players,
                     companies: Companies, privates: dict) -> None:
        """Updates the state of players and companies based on processed row.

        Args:
            row: The parsed line in the full game context.
            players: Player states.
            companies: Company states.
            privates: Privates and their values.
        """
        self._update(row, players, companies, privates)
        players.update(dict(share_prices=companies.share_prices()))
        companies.update(dict())
