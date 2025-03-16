#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from pathlib import Path

from .game_patterns import GamePattern


class GameTranscriptProcessor(object):

    def __init__(self, transcript_file: Path, game: GamePattern):
        self._transcript_file = transcript_file
        self._game = game
        self.data = list()

    def parse_transcript(self):
        """Reads and extracts key actions from the game transcript."""
        with open(self._transcript_file, 'r', encoding='utf-8') as file:
            lines = file.readline()
        for line in lines:
            parsed_data = self._game.extract_pattern(line)
            if parsed_data:
                self.data.append(parsed_data)

    def save_to_dataframe(self):
        """Saves the extracted data as a structured pandas DataFrame."""
        df = pd.DataFrame(self.data)
        df.to_csv('game_data.csv', index=False)
        return df
