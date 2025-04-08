#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pattern mapping algorithm

Module implements caller classes to run all pattern handlers.
"""
from itertools import chain

from . import pattern
from . import actions, events  # noqa


class Patterns(object):
    """Patterns

    TODO
    """

    def __init__(self):
        pass

    @staticmethod
    def _patterns(cls=pattern.PatternHandler):
        # Searches subclasses iteratively.
        return list(chain.from_iterable(
            [list(chain.from_iterable([[x], Patterns._patterns(x)])) for x
             in cls.__subclasses__()])
        )

    @staticmethod
    def _is_abstract(cls):
        # Verifies if class is abstract.
        return bool(getattr(cls, '__abstractmethods__', False))

    def patterns(self):
        """Retrieves pattern handlers.

        Returns:
            Concrete subclasses of the parent class.
        """
        return [cls for cls in self._patterns() if not self._is_abstract(cls)]


class PatternMatcher(object):
    """PatternMatcher

    Class to retrieve and match patterns of all pattern handlers.
    """

    def __init__(self):
        self._algo = Patterns()

    def _search(self, line: str) -> list:
        # Invokes the pattern matching.
        return [cls().match(line) for cls in self._algo.patterns()]

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
        """Matches and processes a line to child patterns.

        Args:
            line: The line to compare to the patterns.

        Returns:
            A dictionary with the found match processed.

        Raises:
            Value: If multiple patterns matched to the line.
        """
        result = self._search(line)
        match = self._select(result, line)
        return match


class PatternProcessor(object):
    """PatternMatcher

    Class to retrieve and match patterns of all pattern handlers.
    """

    def __init__(self):
        self._algo = Patterns()

    def _search(self) -> list:
        # Invokes the pattern types of the subclasses.
        return [cls().type for cls in self._algo.patterns()]

    @staticmethod
    def _select(result: list, pattern_type: pattern.PatternType):

    def run(self, pattern_type: pattern.PatternType) -> dict:
        """
        """
        result = self._search()
        processor = self._select(result, pattern_type)
        return processor
