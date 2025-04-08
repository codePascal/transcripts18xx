#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Game transcript post-processing algorithm

Module implements a post-processing algorithm to clean parsed game transcripts.
"""
import re
import pandas as pd

from pathlib import Path

from .games import Game18xx


class TranscriptPostProcessor(object):
    """TranscriptPostProcessor.

    Class to post-process and clean parsed game transcripts.

    Attributes:
        _df: The parsed transcript.
        _game: The underlying 18xx game.

    Args:
        df: The parsed transcript.
        game: The underlying 18xx game.
    """

    def __init__(self, df: pd.DataFrame, game: Game18xx):
        self._df = df
        self._game = game

        # `round` is not really applicable...
        self._df.rename(columns={'round': 'sequence'}, inplace=True)

    def _map_phase(self):
        # Populates phase with forward propagation.
        self._df.phase = self._df.phase.ffill()

    def _map_rounds(self):
        # Populates rounds with forward propagation.
        if pd.isna(self._df.sequence[0]):
            # Retrieves the initial round identifier from the game.
            self._df.loc[0, 'sequence'] = self._game.initial_round
        self._df.sequence = self._df.sequence.ffill()

    def _remove_transcript_lines(self):
        # Removes the lines from the transcript.
        self._df.drop('line', axis=1, inplace=True)

    def _map_entity(self):
        # Maps the entity to the player or the company column.
        def _entity(row: pd.Series):
            if pd.isna(row.entity):
                pass
            elif row.entity in self._game.companies:
                row.company = row.entity
                return row
            else:
                row.player = row.entity
            return row

        self._df = self._df.apply(lambda x: _entity(x), axis=1)
        self._df.drop('entity', axis=1, inplace=True)

    def _clean_locations(self):
        # Removes the location name from the location identifier.
        self._df.location = self._df.location.apply(
            lambda x: self.clean_brackets(x)
        )

    def _clean_companies(self):
        # Removes the location name from the location identifier.
        self._df.company = self._df.company.apply(
            lambda x: self.clean_brackets(x)
        )

    def process(self) -> None:
        """Processes and cleans the parsed transcript.
        """
        self._map_phase()
        self._map_rounds()
        self._remove_transcript_lines()
        self._map_entity()
        self._clean_locations()
        self._clean_companies()

    def save_to_dataframe(self, transcript_file: Path) -> pd.DataFrame:
        """Saves the processed data as a structured pandas DataFrame.

        The file is saved in the same directory as the transcript and the
        name has `_processed` added in the end. Format is set to .csv with a
        colon a separator.

        Returns:
            The processed data as pandas DataFrame.
        """
        filepath = transcript_file.parent.joinpath(
            transcript_file.stem + '_processed.csv'
        )
        df = pd.DataFrame(self._df)
        df.to_csv(filepath, index=False, sep=',')
        return df

    @staticmethod
    def clean_brackets(bracket_string: str) -> str:
        """Removes the additional information from a string.

        Additional information is stored in brackets after the key string.
        E.g., in locations `E19 (Albany)` or in company names `C&O (D&H)`.

        Args:
            bracket_string: The string which can contain brackets.

        Returns:
            The key data from the string without the data in brackets.
        """
        if pd.isna(bracket_string):
            return bracket_string
        pattern = re.compile(r'(.*?) \(.*?\)')
        match = pattern.search(bracket_string)
        if match:
            return match.group(1)
        return bracket_string
