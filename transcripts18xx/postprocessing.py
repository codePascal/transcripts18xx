#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import pandas as pd

from pathlib import Path

from .states import mapper


class TranscriptPostProcessor(object):

    def __init__(self, df: pd.DataFrame):
        self._df = df

        # `round` is not really applicable...
        self._df.rename(columns={'round': 'sequence'}, inplace=True)

    def _map_phase(self):
        self._df.phase = self._df.phase.fillna(method='ffill')

    def _map_rounds(self):
        self._df.loc[0, 'sequence'] = 'ISR 1'  # only valid for 1830
        self._df.sequence = self._df.sequence.fillna(method='ffill')

    def _map_steps(self):
        self._df['step'] = self._df.apply(lambda x: self._map_type(x), axis=1)
        self._df['step_type'] = self._df.apply(
            lambda x: self._apply_type(x), axis=1
        )
        self._df.drop(['event', 'action'], axis=1, inplace=True)

    @staticmethod
    def _map_type(x: pd.Series) -> str:
        if pd.notna(x.event):
            return x.event
        return x.action

    @staticmethod
    def _apply_type(x: pd.Series) -> str:
        if pd.notna(x.event):
            return 'event'
        return 'action'

    def fill(self):
        self._map_phase()
        self._map_rounds()
        self._map_steps()

    def add_states(self):
        sm = mapper.StatesMapper(self._df)
        sm.map()

    def save_to_dataframe(self, transcript_file: Path) -> pd.DataFrame:
        """Saves the processed data as a structured pandas DataFrame.

        The file is saved in the same directory as the transcript and the
        name has `_processed` added in the end. Format is set to .csv with a
        colon a separator.

        Returns:
            The parsed data as pandas DataFrame.
        """
        filepath = transcript_file.parent.joinpath(
            transcript_file.stem + '_processed.csv'
        )
        df = pd.DataFrame(self._df)
        df.to_csv(filepath, index=False, sep=',')
        return df
