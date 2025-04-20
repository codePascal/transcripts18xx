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
        _engine: The line parser engine.
    """

    def __init__(self):
        self._engine = engine.LineParser()

    @staticmethod
    def _preprocess_line(line: str) -> str:
        # Sometimes there is a timestamp [hh:mm], cut it
        if line.startswith('['):
            line = line[8:]
        line = line.lstrip()
        return line

    def parse_transcript(self, transcript_file: Path) -> pd.DataFrame:
        """Reads and extracts actions and events from the game transcript.

        Args:
            transcript_file: The filepath to the transcript.

        Returns:
            The parsed transcript.
        """
        data = list()
        with open(transcript_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        unprocessed = list()
        for i, line in enumerate(lines):
            line = self._preprocess_line(line)
            parsed_data = self._engine.run(line)
            if parsed_data:
                parsed_data['id'] = i
                parsed_data['line'] = line
                data.append(parsed_data)
            else:
                unprocessed.append(line.strip())
        if unprocessed:
            print('Unprocessed lines:')
            print('\n'.join(unprocessed))
        return pd.DataFrame(data)
