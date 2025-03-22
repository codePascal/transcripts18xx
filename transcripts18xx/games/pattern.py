#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pattern.py

Module implements an abstract class to define and search for game patterns.
"""
import abc


class GamePattern(abc.ABC):
    """GamePattern

    Class to define game patterns, i.e. how the lines of a transcript shall be
    parsed. Each event and possible actions that appear in the transcript
    are implemented as regular expression matching operations. This class
    receives a transcript line and checks the linked expressions for a match.
    """

    def __init__(self):
        pass

    @staticmethod
    def _match(matches: list[dict | None]) -> dict | None:
        # Extracts the found match of the parse recipe.
        match = [m for m in matches if m is not None]
        if not match:
            # This is bad: a transcript line could not be matched!
            return None
        if len(match) != 1:
            # This is bad as well: more than one recipe resulted in a match!
            raise IndexError('More than one match: {}'.format(match))
        return match[0]

    @abc.abstractmethod
    def _check_events(self, line: str) -> dict | None:
        # Checks the events recipes for a match.
        pass

    @abc.abstractmethod
    def _check_actions(self, line: str) -> dict | None:
        # Checks the actions recipes for a match.
        pass

    @abc.abstractmethod
    def extract_pattern(self, line: str) -> dict | None:
        """Parses the line and checks for matches in the given recipes.

        Args:
            line: A transcript line to parse.

        Returns:
            If a match is found, returns the result parsed in a dictionary.
            Otherwise, returns None.
        """
        pass
