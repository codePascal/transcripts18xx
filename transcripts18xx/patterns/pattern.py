#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic pattern matching and processing.

Module implements abstract base classes to match patterns to a string and
run some post-processing on the line if a match was found.
"""
import abc
import enum
import re


class PatternType(enum.IntEnum):
    """PatternType

    Enum class to describe a pattern by a type.
    """
    pass


class PatternParent(enum.IntEnum):
    """PatternParent

    Enum class to describe a group of patterns.
    """
    Event = 0
    Action = 1


class PatternHandler(abc.ABC):
    """PatternHandler

    EngineStep

    Class to map a line to a pattern. Each subclass implements a pattern, that
    is compared to a line. The pattern is implemented as a regular expression.

    todo Child .. implement one action --> subs but return equal to parent...

    Attributes:
        pattern: The expression that shall be matched to the line.
        type: The type of the pattern, see `PatternType`.
        parent: The pattern group the pattern is part of, see `PatternParent`.
        _dismiss: Keywords that result in the line being ignored if they exist
            in the line.
        _required: Keywords that need to be found in the line. Otherwise, the
            line is ignored. If multiple keywords are given, only one must be
            found for the line to be checked.
    """

    def __init__(self):
        self.pattern = None
        self.type = PatternType
        self.parent = PatternParent

        self._dismiss = list()
        self._required = list()

    def _search(self, line: str) -> re.Match | None:
        # Invokes the search command.
        if self.pattern is None:
            return None
        return self.pattern.search(line)

    @abc.abstractmethod
    def _handle(self, line: str, match) -> dict:
        # Processes the match.
        pass

    def _contains_dismiss_key(self, line: str) -> bool:
        # Checks if key to dismiss exists in line as single word.
        return any(key in line.split() for key in self._dismiss)

    def _contains_required_key(self, line: str) -> bool:
        # Checks if required key exists in line as single word.
        return any(key in line.split() for key in self._required)

    def search(self, line: str) -> re.Match | None:
        """Maps the pattern to the line and searches for a match.

        Args:
            line: The line to compare to the pattern.

        Returns:
            A match if found or None.
        """
        if self._contains_dismiss_key(line):
            return None
        if not self._required or self._contains_required_key(line):
            return self._search(line)
        return None

    def handle(self, line: str, match) -> dict:
        """Processes the line and its matches.

        Args:
            line: The line that resulted in a match.
            match: The matches found by the regex.

        Returns:
            A dictionary with the matches processed.
        """
        ret = self._handle(line, match)
        ret['type'] = self.type.name
        ret['parent'] = self.parent.name
        return ret

    def match(self, line: str) -> dict | None:
        """Matches and processes a line to the pattern.

        Args:
            line: The line to compare to the pattern.

        Returns:
            A dictionary with the matches processed, or None if no match found.
        """
        match = self.search(line)
        if match:
            return self.handle(line, match)
        return None
