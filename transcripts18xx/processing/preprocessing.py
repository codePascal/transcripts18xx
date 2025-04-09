#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Game transcript preprocessing algorithm

Module implements a transcript processor to process and parse game transcripts
from 18xx.games.
"""
import pandas as pd

from pathlib import Path

from ..engine import engine


class GameTranscriptProcessor(object):
    """GameTranscriptProcessor

    Class to process and parse game transcripts.

    Attributes:
        _transcript_file: The transcript file path.
        _data: Data container to save the processed lines as dicts.

    Args:
        transcript_file: The transcript file path.
    """

    def __init__(self, transcript_file: Path):
        self._transcript_file = transcript_file
        self._engine = engine.LineParser()
        self._data = list()

    @staticmethod
    def _preprocess_line(line: str) -> str:
        # Sometimes there is a timestamp [hh:mm], cut it
        if line.startswith('['):
            line = line[8:]
        line = line.lstrip()
        return line

    def parse_transcript(self) -> None:
        """Reads and extracts actions and events from the game transcript.
        """
        with open(self._transcript_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        unprocessed = list()
        for i, line in enumerate(lines):
            line = self._preprocess_line(line)
            parsed_data = self._engine.run(line)
            if parsed_data:
                parsed_data['id'] = i
                parsed_data['line'] = line
                self._data.append(parsed_data)
            else:
                unprocessed.append(line)
        if unprocessed:
            print('Unprocessed lines:')
            print('\n'.join(unprocessed))

    def save_to_dataframe(self) -> pd.DataFrame:
        """Saves the extracted data as a structured pandas DataFrame.

        The file is saved in the same directory as the transcript and the
        name has `_parsed` added in the end. Format is set to .csv with a
        colon a separator.

        Returns:
            The parsed data as pandas DataFrame.
        """
        filepath = self._transcript_file.parent.joinpath(
            self._transcript_file.stem + '_parsed.csv'
        )
        df = pd.DataFrame(self._data)
        df.to_csv(filepath, index=False, sep=',')
        return df
