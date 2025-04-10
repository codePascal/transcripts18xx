#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Game transcript game state algorithm

Module implements an algorithm to map game states to the cleaned and processed
transcript.
"""
import pandas as pd

from pathlib import Path

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
            df.player.dropna().unique(), df.company.dropna().unique()
        )
        self._steps = engine.StepMapper()

    def generate(self):
        for i, row in self._df.iterrows():
            step_type = self._steps.map_type(row.type)
            step_engine = self._steps.run(step_type)
            self._game_state.update(row, step_engine())

    def save_to_dataframe(self, transcript_file: Path) -> pd.DataFrame:
        """Saves the final data as a structured pandas DataFrame.

        The file is saved in the same directory as the transcript and the
        name has `_final` added in the end. Format is set to .csv with a
        colon a separator.

        Returns:
            The final data as pandas DataFrame.
        """
        filepath = transcript_file.parent.joinpath(
            transcript_file.stem + '_final.csv'
        )
        df = pd.DataFrame(self._df)
        df.to_csv(filepath, index=False, sep=',')
        return df
