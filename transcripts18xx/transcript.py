#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Transcript processing pipeline

Module implements the transcript processing pipeline with parsing the
transcript, processing the result and mapping player and company states.

The transcript name must follow this rule: `<title>_<id>.txt`.
E.g.: `1830_201210.txt`, where `1830` is the title or the game and `201210` is
the ID of the game.
"""
import json
import pandas as pd

from pathlib import Path

from . import parsing, games


class TranscriptParser(object):

    def __init__(self, transcript: Path, game: games.Game18xx):
        self._transcript = transcript
        self._game = game

        self._mapping = dict()
        self._df = pd.DataFrame()

    def _game_info(self):
        # Builds the game info.
        info = dict()
        game_type, game_id = self._transcript.stem.split('_')
        info['game'] = game_type
        info['id'] = game_id
        info['num_players'] = len(self._mapping.keys())
        info['players'] = {v: k for k, v in self._mapping.items()}
        return info

    def _write_result(self):
        # Writes the results to .csv file.
        self._df.to_csv(
            self._transcript.parent.joinpath(
                self._transcript.stem + '_final.csv'
            ),
            index=False,
            sep=','
        )

    def _write_metadata(self):
        # Writes the game info to .json file.
        file = self._transcript.parent.joinpath(
            self._transcript.stem + '_metadata.json'
        )
        with open(file, 'w') as f:
            f.write(json.dumps(self._game_info(), indent=2))

    def parse(self) -> pd.DataFrame:
        """Parses the transcript to a pandas Dataframe.

        Returns:
            The parsed data in a pandas Dataframe.
        """
        gtp = parsing.GameTranscriptProcessor()
        df_parsed = gtp.parse_transcript(self._transcript)

        tpp = parsing.TranscriptPostProcessor(df_parsed, self._game)
        df_processed, mapping = tpp.process()
        self._mapping = mapping

        gsp = parsing.GameStateProcessor(df_processed, self._game)
        df_final = gsp.generate()
        self._df = df_final
        return df_final

    def verify_result(self, minimal: bool = False) -> bool:
        """Verifies the result

        Args:
            minimal:

        Returns:

        """
        verification_file = Path(self._transcript.stem + '.json')
        if not verification_file.exists():
            raise ValueError('...')
        pass

    def save(self):
        """Saves the game data and its metadata.

        The game data is saved as .csv file: `_final.csv`. The metadata is saved
        as .json file: `_metadata.json`.
        """
        self._write_result()
        self._write_metadata()

    def serialize(self):
        """Saves the game data including metadata.

        Both are incorporated into a .json file: `_serialized.json`.
        """
        result = self._game_info()
        result['actions'] = self._df.to_dict(orient='index')
        file = self._transcript.parent.joinpath(
            self._transcript.stem + '_serialized.json'
        )
        with open(file, 'w') as f:
            f.write(json.dumps(result, indent=2))
