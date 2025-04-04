#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pattern.py

Module implements an abstract class to define and search for game patterns.
"""
import abc

from ..patterns.actions import actions
from ..patterns.events import events


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
    def _check_events(line: str) -> dict | None:
        # Checks the events recipes for a match.
        return GamePattern.match(events.events(line))

    @staticmethod
    def _check_actions(line: str) -> dict | None:
        # Checks the actions recipes for a match.
        return GamePattern.match(actions.actions(line))

    def extract_pattern(self, line: str) -> dict | None:
        """Parses the line and checks for matches in the given recipes.

        Args:
            line: A transcript line to parse.

        Returns:
            If a match is found, returns the result parsed in a dictionary.
            Otherwise, returns None.
        """
        return self.match([
            self._check_events(line),
            self._check_actions(line)
        ])

    @staticmethod
    def match(matches: list[dict | None]) -> dict | None:
        """Screens a list of pattern results and finds the match.

        Args:
            matches: List of checked patterns; Ideally only one match was found.

        Returns:
            The found match if one available or None if no match was found.

        Raises:
            IndexError: If more than one match was found.
        """
        match = [m for m in matches if m is not None]
        if not match:
            # This is bad: a transcript line could not be matched!
            return None
        if len(match) != 1:
            # This is bad as well: more than one recipe resulted in a match!
            error_str = '\n'.join([m.__str__() for m in match])
            raise IndexError('More than one match:\n{}'.format(error_str))
        return match[0]
