#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Engine algorithm for matching and processing

Module implements caller classes to run all step handlers on a specific
function or retrieve the members.
"""
from itertools import chain
from typing import Type

import pandas as pd

from ..games import Game18xx
from .steps import step
from .steps import actions, events  # noqa
from .states import player, company


class EngineSteps(object):
    """EngineSteps

    Class to retrieve all available engine steps, which are concrete subclasses
    of EngineStep.
    """

    def __init__(self):
        pass

    @staticmethod
    def _patterns(cls=step.EngineStep):
        # Searches subclasses iteratively.
        return list(chain.from_iterable(
            [list(chain.from_iterable([[x], EngineSteps._patterns(x)])) for x
             in cls.__subclasses__()])
        )

    @staticmethod
    def _is_abstract(cls):
        # Verifies if class is abstract.
        return bool(getattr(cls, '__abstractmethods__', False))

    def patterns(self):
        """Retrieves engine steps.

        Returns:
            Concrete subclasses of the parent class.
        """
        return [cls for cls in self._patterns() if not self._is_abstract(cls)]


class LineParser(object):
    """LineParser

    Class to retrieve and match a line to all engine steps.

    Attributes:
        _steps: Engine steps to match.
    """

    def __init__(self):
        self._steps = EngineSteps().patterns()

    def _search(self, line: str) -> list:
        # Invokes the pattern matching.
        return [cls().match(line) for cls in self._steps]

    @staticmethod
    def _select(result: list, line: str) -> dict | None:
        # Retrieves the match from the search result.
        matches = [ret for ret in result if ret is not None]
        if len(matches) > 1:
            raise ValueError(
                'Multiple matches found for line `{}`:\n{}'.format(
                    line,
                    '\n'.join(m.__str__() for m in matches)
                )
            )
        if not matches:
            return None
        return matches[0]

    def run(self, line: str) -> dict | None:
        """Matches and processes the line to engine steps.

        Args:
            line: The line to compare to the steps.

        Returns:
            A dictionary with the found match processed, or None if no match
            was found.

        Raises:
            ValueError: If multiple steps matched to the line.
        """
        result = self._search(line)
        match = self._select(result, line)
        return match


class StepMapper(object):
    """StepMapper

    Class to match a step name to its engine.

    Attributes:
        _steps: Engine steps.
    """

    def __init__(self):
        self._steps = EngineSteps().patterns()

    def _search(self, step_type: step.StepType) -> list:
        # Invokes the step type name of the subclasses.
        return [
            cls for cls in self._steps if cls().type.name == step_type.name
        ]

    @staticmethod
    def _select(result: list) -> Type[step.EngineStep]:
        # Selects the parent of the engine steps.
        if len(result) == 1:
            return result[0]
        else:
            # Return the parent class which is in the first position.
            return result[0]

    def run(self, step_type: step.StepType) -> Type[step.EngineStep]:
        """Maps an engine to its step name.

        Args:
            step_type: Step to match.

        Returns:
            The engine for the step.
        """
        result = self._search(step_type)
        engine = self._select(result)
        return engine

    @staticmethod
    def map_type(step_name: str) -> step.StepType:
        """Maps the step name to its enum member.

        Args:
            step_name: Name of the step.

        Returns:
            The matching enum member.
        """
        try:
            result = actions.Actions[step_name]
        except KeyError:
            try:
                result = events.Events[step_name]
            except KeyError:
                raise KeyError(
                    'No matching engine step found: {}'.format(step_name)
                )
        return result


class GameState(object):

    def __init__(self, players: list[str], companies: list[str],
                 game: Game18xx):
        self.players = player.Players(
            players, game.companies, game.start_capital
        )
        self.companies = company.Companies(companies, game.trains)
        self.privates = game.privates

    def update(self, row: pd.Series, engine: step.EngineStep):
        engine.state_update(row, self.players, self.companies, self.privates)
        self.players.update(dict(share_prices=self.companies.share_prices()))
        self.companies.update(dict())

    def view(self):
        return {**self.players.as_dict(), **self.companies.as_dict()}
