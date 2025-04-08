#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Engine algorithm for matching and processing

Module implements caller classes to run all step handlers on a specific
function or retrieve the members.
"""
from itertools import chain
from typing import Type

from .steps import step
from .steps import actions, events  # noqa


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
    def _select(result: list, line: str) -> dict:
        # Retrieves the match from the search result.
        matches = [ret for ret in result if ret is not None]
        if len(matches) > 1:
            raise ValueError(
                'Multiple matches found for line `{}`:\n{}'.format(
                    line,
                    '\n'.join(m.__str__() for m in matches)
                )
            )
        return matches[0]

    def run(self, line: str) -> dict:
        """Matches and processes the line to engine steps.

        Args:
            line: The line to compare to the steps.

        Returns:
            A dictionary with the found match processed.

        Raises:
            Value: If multiple steps matched to the line.
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
