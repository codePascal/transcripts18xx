#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Transcript processing pipeline

Module implements the transcript processing pipeline with parsing the
transcript, processing the result and mapping player and company states.

The transcript name must follow this rule: `<title>_<id>.txt`.
E.g.: `1830_201210.txt`, where `1830` is the title of the game and `201210` is
the ID of the game.
"""
import json
import pandas as pd

from pathlib import Path

from . import parsing, games, verification


class TranscriptParser(object):
    """TranscriptParser

    Class to run the parsing pipeline. The result can be verified with a
    file representing the truth of the final states (full) or using the final
    value of each player (minimal). Parsed results, game metadata and final
    states can be written to files for later usage.

    Attributes:
        _transcript: The path to the game transcript.
        _game: The underlying 18xx game.
        _name: The name of the transcript file, excluding suffix.
        _dir: The parent directory of the transcript.
        _mapping: The player name mapping.
        _df: The parsed transcript data.
        _final_state: The final states of players and companies.

    Args:
        transcript: The filepath to the transcript.
        game: The underlying 18xx game, see `games.G18xx`.
    """

    def __init__(self, transcript: Path, game: games.Game18xx):
        self._transcript = transcript
        self._game = game

        self._name = transcript.stem
        self._dir = transcript.parent

        self._mapping = dict()
        self._df = pd.DataFrame()
        self._final_state = dict()

    def _game_info(self):
        # Builds the game info.
        info = dict()
        game_type, game_id = self._name.split('_')
        info['game'] = game_type
        info['id'] = game_id
        info['num_players'] = len(self._mapping.keys())
        info['players'] = {v: k for k, v in self._mapping.items()}
        return info

    def _write_result(self):
        # Writes the results to .csv file.
        self._df.to_csv(
            self._dir.joinpath(self._name + '_final.csv'),
            index=False,
            sep=','
        )

    def _write_metadata(self):
        # Writes the game info to .json file.
        with open(self._dir.joinpath(self._name + '_metadata.json'), 'w') as f:
            f.write(json.dumps(self._game_info(), indent=2))

    def _write_states(self):
        # Writes the final states to .json file.
        with open(self._dir.joinpath(self._name + '_states.json'), 'w') as f:
            f.write(json.dumps(self.final_state(anonym=False), indent=2))

    def _replace(self, obj, old, new):
        # Replaces the old with the new value in object.
        if isinstance(obj, dict):
            return {
                k.replace(old, new): self._replace(v, old, new) for k, v in
                obj.items()
            }
        elif isinstance(obj, list):
            return [self._replace(item, old, new) for item in obj]
        elif isinstance(obj, str):
            return obj.replace(old, new)
        else:
            return obj

    def _run_full_verification(self) -> bool:
        # Run the full verification based on a ground truth file.
        verification_file = self._dir.joinpath(self._name + '_truth.json')
        if not verification_file.exists():
            raise ValueError(
                'No verification file with ground truth exist: {}'.format(
                    verification_file
                )
            )
        with open(verification_file, 'r') as f:
            truth = json.load(f)
        checker = verification.StateVerification()
        ret = checker.run(self.final_state(anonym=False), truth)
        return ret

    def _run_minimal_verification(self) -> bool:
        # Run the minimal verification comparing final value of the players.
        transcript_result = eval(self._df.iloc[-1].result)
        game_state_result = dict()
        for k, v in self._final_state['players'].items():
            game_state_result[k] = int(v['value'])
        checker = verification.StateVerification()
        ret = checker.run(game_state_result, transcript_result)
        return ret

    def parse(self) -> pd.DataFrame:
        """Parses the transcript to a pandas Dataframe.

        Returns:
            The parsed data in a pandas Dataframe.
        """
        gtp = parsing.GameTranscriptProcessor()
        df_parsed = gtp.parse_transcript(self._transcript)

        tpp = parsing.TranscriptPostProcessor(df_parsed, self._game)
        df_processed, self._mapping = tpp.process()

        gsp = parsing.GameStateProcessor(df_processed, self._game)
        self._df = gsp.generate()
        self._final_state = gsp.final_state()
        return self._df

    def final_state(self, anonym: bool = False) -> dict:
        """Extracts the final state of the players and companies.

        Args:
            anonym: Set to True to anonymize the player names. Otherwise,
                players will be identified by their names.

        Returns:
            The final states as dictionaries.
        """
        final = self._final_state
        if not anonym:
            for name, abbrev in self._mapping.items():
                final = self._replace(final, abbrev, name)
        return final

    def verify_result(self, minimal: bool = False) -> bool:
        """Verifies the result with the final state.

        If option minimal is selected, compares the final value of the players
        parsed from the transcript to the one retrieved from the game state.
        Otherwise, compares the player and company states to a ground truth
        file `_truth.json`, saved in the transcript directory. If the file is
        not found, the minimal verification is invoked automatically.

        Args:
            minimal: Run only minimal verification.

        Returns:
            True if final states are equal, False otherwise.
        """
        if minimal:
            ret = self._run_minimal_verification()
            out = 'Minimal verification {}'
        else:
            try:
                ret = self._run_full_verification()
                out = 'Full verification {}'
            except ValueError:
                print(
                    'Ground truth file not found, running minimal verification'
                )
                ret = self._run_minimal_verification()
                out = 'Minimal verification {}'
        if ret:
            print(out.format('successful') + '\n')
        else:
            print(out.format('failed') + '\n')
        return ret

    def save(self):
        """Saves the game data, its metadata and the final states.

        The files are saved in the transcript directory:
            - game data: `_final.csv`
            - metadata: `_metadata.json`
            - final states: `_states.json`

        The final states are not anonymized.
        """
        self._write_result()
        self._write_metadata()
        self._write_states()

    def serialize(self):
        """Saves the game data including metadata and final states.

        The file is saved in the transcript directory with `_serialized.json`
        appended. The final states are anonymized.
        """
        result = self._game_info()
        result['actions'] = self._df.to_dict(orient='index')
        result['results'] = self.final_state(anonym=True)
        with open(
                self._dir.joinpath(self._name + '_serialized.json'), 'w'
        ) as f:
            f.write(json.dumps(result, indent=2))
