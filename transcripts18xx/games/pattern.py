#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc


class GamePattern(abc.ABC):

    def __init__(self):
        pass

    @staticmethod
    def _match(matches: list[dict | None]) -> dict | None:
        match = [m for m in matches if m is not None]
        if not match:
            return None
        return match[0]

    @abc.abstractmethod
    def _check_events(self, line: str) -> dict | None:
        pass

    @abc.abstractmethod
    def _check_actions(self, line: str) -> dict | None:
        pass

    @abc.abstractmethod
    def extract_pattern(self, line: str) -> dict | None:
        pass
