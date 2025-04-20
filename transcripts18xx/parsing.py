#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Game transcript preprocessing algorithm

Module implements a transcript processor to process and parse game transcripts
from 18xx.games.
"""
import pandas as pd
import re

from pathlib import Path

from .games import Game18xx
from .engine import engine


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

    def _anonymize(self) -> dict:
        # Replace player names with normalized names.
        mapping = {
            p: 'player{}'.format(i + 1) for i, p in
            enumerate(self._df.player.dropna().unique()) if not pd.isna(p)
        }
        self._df.replace(mapping.keys(), mapping.values(), inplace=True)
        return mapping

    def process(self) -> tuple[pd.DataFrame, dict]:
        """Processes and cleans the parsed transcript.

        Returns:
            The processed transcript data and the player mapping.
        """
        self._map_phase()
        self._map_rounds()
        self._remove_transcript_lines()
        self._map_entity()
        self._clean_locations()
        self._clean_companies()
        mapping = self._anonymize()
        return self._df, mapping

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
