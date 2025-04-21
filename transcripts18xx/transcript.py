#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Transcript processing pipeline

Module implements the transcript processing pipeline with parsing the
transcript, processing the result and mapping player and company states.

The transcript name must follow this rule: `<title>_<id>.txt`.
E.g.: `1830_201210.txt`, where `1830` is the title or the game and `201210` is
the ID of the game.
"""
import pandas as pd

from pathlib import Path

from . import parsing, games

# TODO:
#   * parse
#   * save as df or json (argument)
#   * add game data (id, type, num players, etc.)

"""
from game data output
{
  "id": 201210,
  "description": "",
  "user": {
    "id": 15781,
    "name": "leesin"
  },
  "players": [
    {
      "id": 19333,
      "name": "mpcoyne"
    },
    {
      "id": 18933,
      "name": "riverfiend"
    },
    {
      "id": 15781,
      "name": "leesin"
    },
    {
      "id": 18620,
      "name": "mpakfm"
    }
  ],
  "min_players": 4,
  "max_players": 6,
  "title": "1830",
  "settings": {
    "seed": 752300876,
    "is_async": false,
    "unlisted": false,
    "auto_routing": true,
    "player_order": null,
    "optional_rules": []
  },
  "user_settings": null,
  "status": "finished",
  "turn": 8,
  "round": "Operating Round",
  "acting": [
    19333,
    18933,
    15781,
    18620
  ],
  "result": {
    "15781": 6648,
    "18620": 2740,
    "18933": 5523,
    "19333": 6735
  },
"""


class TranscriptParser(object):

    def __init__(self, transcript: Path, game: games.Game18xx):
        self._transcript = transcript
        self._game = game

        self._mapping = dict()
        self._df = pd.DataFrame()

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
        return df_final

    def verify_result(self, df: pd.DataFrame, minimal: bool = False) -> bool:
        verification_file = Path(self._transcript.stem + '.json')
        if not verification_file.exists():
            raise ValueError('...')
        pass

    def save(self, df: pd.DataFrame):
        filename = Path(self._transcript.stem + '_final.csv')
        print(filename)

    def serialize(self, df: pd.DataFrame):
        # Json encoded
        filename = Path(self._transcript.stem + '_final.json')
        print(filename)
        pass
