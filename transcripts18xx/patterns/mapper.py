#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pattern mapping algorithm

Module implements caller class to run all pattern handlers on a line.
"""
from itertools import chain

from . import pattern
from . import actions, events  # noqa


class PatternMatcher(object):
    """PatternMatcher

    Class to retrieve and match patterns of all pattern handlers.
    """

    def __init__(self):
        self._cls = pattern.PatternHandler

    def _get_patterns(self):
        # Returns the concrete pattern subclasses.
        return [
            cls for cls in self.patterns(self._cls) if not self.is_abstract(cls)
        ]

    def _search(self, line: str) -> list:
        # Invokes the pattern matching.
        return [cls().match(line) for cls in self._get_patterns()]

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

    @staticmethod
    def patterns(cls):
        """Retrieves all subclasses of a parent class.

        Args:
            cls: Parent class.

        Returns:
            Subclasses of the parent class.
        """
        return list(chain.from_iterable(
            [list(chain.from_iterable([[x], PatternMatcher.patterns(x)])) for x
             in cls.__subclasses__()])
        )

    @staticmethod
    def is_abstract(cls):
        """Verifies if a class is an abstract class.

        Args:
            cls: The class to verify.

        Returns:
            True if class is abstract, False otherwise.
        """
        return bool(getattr(cls, '__abstractmethods__', False))

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
