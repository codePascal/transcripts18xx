#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Game transcript parser algorithm

Module implements classes that build the algorithm to parse a transcript from
18xx.games and map the current game state to each line. The algorithm consist
of a parser to handle the raw transcript, a processor that cleans and
post-processes the transcript and a mapper for the game state.
"""
import pandas as pd
import re

from pathlib import Path

from .games import Game18xx
from .engine import engine


class GameTranscriptProcessor(object):
    """GameTranscriptProcessor

    Class to process and parse game transcripts. The class invokes a line parser
    that checks the lines against all step engines and finds the hopefully
    unique match. Lines that were not matched are printed to the console. The
    parsed lines are combined in a pandas Dataframe.

    Attributes:
        _engine: The line parser engine.
    """

    def __init__(self):
        self._engine = engine.LineParser()

    def _process_line(self, idx: int, line: str, data: list, unprocessed: list):
        line = self._preprocess_line(line)
        parsed_data = self._engine.run(line)
        if parsed_data:
            parsed_data['id'] = idx
            parsed_data['line'] = line
            data.append(parsed_data)
        else:
            unprocessed.append(line.strip())

    @staticmethod
    def _preprocess_line(line: str) -> str:
        # Sometimes there is a timestamp [hh:mm], cut it.
        if line.startswith('['):
            line = line[8:]
        line = line.lstrip()
        return line

    @staticmethod
    def _read_transcript(transcript: Path) -> list[str]:
        with open(transcript, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines

    @staticmethod
    def _handle_unprocessed_lines(unprocessed: list):
        print('Unprocessed lines:')
        print('\n'.join(unprocessed))

    def parse_transcript(self, transcript: Path) -> pd.DataFrame:
        """Reads and extracts actions and events from the game transcript.

        Args:
            transcript: The filepath to the transcript.

        Returns:
            The parsed transcript as pandas Dataframe.
        """
        data = list()
        unprocessed = list()
        for i, line in enumerate(self._read_transcript(transcript)):
            self._process_line(i, line, data, unprocessed)
        if unprocessed:
            self._handle_unprocessed_lines(unprocessed)
        return pd.DataFrame(data)


class TranscriptPostProcessor(object):
    """TranscriptPostProcessor

    Class to post-process and clean parsed game transcripts. The class fills up
    the phase and round keys which are valid until the next key arrives. It
    further maps and renders columns which require the game context, given by
    the type of game and the whole parsed transcript. To this end, the player
    names are anonymized for better generalization.

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

    def _map_dtypes(self) -> None:
        self._df.amount = self._df.amount.astype(float)
        self._df.percentage = self._df.percentage.astype(float)
        self._df.share_price = self._df.share_price.astype(float)
        self._df.per_share = self._df.per_share.astype(float)

    def _anonymize(self) -> dict:
        # Replace player names with normalized names.
        mapping = {
            p: 'player{}'.format(i + 1) for i, p in
            enumerate(self._df.player.dropna().unique()) if not pd.isna(p)
        }
        self._df.replace(mapping.keys(), mapping.values(), inplace=True)

        # Replace the keys of the result when game over was reached
        result = eval(self._df.iloc[-1].result)
        renamed = {mapping[k]: v for k, v in result.items()}
        self._df.at[self._df.shape[0] - 1, 'result'] = renamed.__str__()

        return mapping

    def _set_contribute_target(self) -> None:
        contributions = self._df[
            self._df['type'] == engine.step.StepType.Contribute.name
            ].index.tolist()
        for cont in contributions:
            # Next action after contribution is buy a train
            next_action = self._df.iloc[cont + 1, :]
            if not next_action['type'] == engine.step.StepType.BuyTrain.name:
                raise ValueError(
                    'Can not set target for contribution: {}'.format(
                        next_action.to_string()
                    )
                )

            # Map the company that receives the contribution
            this_action = self._df.iloc[cont, :].copy()
            this_action.company = next_action.company
            self._df.iloc[cont, :] = this_action

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
        self._map_dtypes()
        self._set_contribute_target()
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
    """GameStateProcessor

    Class to map the game state to the cleaned and processed transcript. The
    game state consist of the player and company states at each entry of the
    transcript. Some columns in the processed transcript could become obsolete,
    but for completeness, these will not be removed.

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
            df.player.dropna().unique(),
            df.company.dropna().unique(),
            game.start_capital,
            game.trains,
            game.privates
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

    def final_state(self) -> dict:
        """Extracts the final state of players and companies.

        Returns:
            The dictionary representing states of players and companies.
        """
        return {
            **self._game_state.player_states(),
            **self._game_state.company_states()
        }
