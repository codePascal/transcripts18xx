#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Game transcript game state algorithm

Module implements an algorithm to map game states to the cleaned and processed
transcript.
"""
import pandas as pd

from ..games import Game18xx
from ..engine import engine


class GameStateProcessor(object):
    """GameStateProcessor.

    Class to map the game state to the cleaned and processed transcript.

    Attributes:
        _df: The cleaned and processed transcript.
        _game: The underlying 18xx game.

    Args:
        df: The cleaned and processed transcript.
        game: The underlying 18xx game.
    """

    def __init__(self, df: pd.DataFrame, game: Game18xx):
        self._df = df
        self._game = game

        self._game_state = engine.GameState(
            df.player.dropna().unique(), df.company.dropna().unique(), game
        )
        self._steps = engine.StepMapper()

    def _update(self, row: pd.Series):
        # Update a row with its step engine and return the game state.
        step_type = self._steps.map_type(row.type)
        step_engine = self._steps.run(step_type)
        self._game_state.update(row, step_engine())
        return self._game_state.view()

    def generate(self) -> pd.DataFrame:
        """Generate and add the game state for each step.

        Returns:
            Final transcript with game state added.
        """
        state = self._df.apply(
            lambda x: self._update(x), axis=1, result_type='expand'
        )
        self._df = pd.concat([self._df, state], axis=1)
        return self._df
