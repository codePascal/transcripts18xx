#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
import enum
import re

from itertools import chain


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

    Class to map a line to a pattern. Each subclass implements a pattern, that
    is compared to a line. The pattern is implemented as a regular expression.

    Attributes:
        pattern: The expression that shall be matched to the line.
        type: The type of the pattern, see `PatternType`.
        parent: The pattern group the pattern is part of, see `PatternParent`.
        _dismiss: Keywords that result in the line being ignored if they exist
            in the line.
        _required: Keywords that need to be found in the line. Otherwise the
            line is ignored.
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
        if not self._required:
            return True
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


class MatchException(Exception):
    pass


class PatternMatcher(abc.ABC):
    """PatternMatcher

    Class to retrieve and match patterns of a parent class to a line.

    Args:
        cls: The parent class to match patterns.
    """

    def __init__(self, cls):
        self._cls = cls

    def _get_patterns(self):
        # Returns the concrete pattern subclasses.
        return [
            cls for cls in self.patterns(self._cls) if not self.is_abstract(cls)
        ]

    def _search(self, line: str) -> list:
        # Invokes the pattern matching.
        return [cls().match(line) for cls in self._get_patterns()]

    @staticmethod
    def _select(result: list) -> dict:
        # Retrieves the match from the search result.
        matches = [ret for ret in result if ret is not None]
        if len(matches) > 1:
            raise MatchException(
                'Multiple matches found:\n{}'.format(
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
            MatchException: If multiple patterns matched to the line.
        """
        result = self._search(line)
        match = self._select(result)
        return match

        # TODO: map class to action
