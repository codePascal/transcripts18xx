#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from pathlib import Path

from transcripts18xx.games.pattern import GamePattern


class GameTranscriptProcessor(object):

    def __init__(self, transcript_file: Path, game: GamePattern):
        self._transcript_file = transcript_file
        self._game = game
        self.data = list()

    def parse_transcript(self):
        """Reads and extracts key actions from the game transcript."""
        with open(self._transcript_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            parsed_data = self._game.extract_pattern(line)
            if parsed_data:
                parsed_data['id'] = i
                self.data.append(parsed_data)
            else:
                print(line)

    def save_to_dataframe(self):
        """Saves the extracted data as a structured pandas DataFrame."""
        df = pd.DataFrame(self.data)
        df.to_csv(
            Path(__file__).parent.parent.joinpath('game_state.csv'),
            index=False,
            sep=','
        )
        return df
