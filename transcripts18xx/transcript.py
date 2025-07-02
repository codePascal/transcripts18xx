#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Transcript processing pipeline

Module implements the transcript processing pipeline with parsing the
transcript, processing the result and mapping player and company states.
Further, implements functions to access results based on the raw
transcript name and run full verification on these.
"""
import json
import pandas as pd
import ast
import logging

from pathlib import Path

from . import games
from .pipe import parsing, verification
from .engine.steps.step import StepType

logger = logging.getLogger(__name__)


class TranscriptParser(object):
    """TranscriptParser

    Class to run the parsing pipeline. Verifies the final values of the players
    with the result in the game log in case the game was finished. Parsed
    transcript and its metadata are saved in the raw transcript folder.

    Attributes:
        _transcript: The path to the game transcript.
        _game: The underlying 18xx game.
        _metadata: The metadata to the parsing result.
        _df: The parsed transcript data.

    Args:
        transcript: The filepath to the transcript.
        game: The underlying 18xx game, see `games.G18xx`.
    """

    def __init__(self, transcript: Path, game: games.Game18xx):
        self._transcript = transcript
        self._game = game

        self._metadata = dict()
        game_type, game_id = transcript.stem.split('_')
        self._metadata['game'] = game_type
        self._metadata['id'] = game_id

        self._df = pd.DataFrame()

    def _anonymize_players(self) -> dict:
        # Map the player names to general format `playerx`.
        players = self._df.player.dropna().unique()
        mapping = {p: 'player{}'.format(i + 1) for i, p in enumerate(players)}
        return mapping

    def _anonymize(self, obj):
        # Anonymize a data container with the general mapping format.
        for old, new in self._metadata['mapping'].items():
            obj = _replace(obj, old, new)
        return obj

    def _evaluate_last_state(self) -> dict:
        # Evaluate the last state if finished and the results.
        last_state = dict(
            finished=str(),
            result=dict(),
            winner=str()
        )
        if self._df.type.iloc[-1] != StepType.GameOver.name:
            last_state['finished'] = 'NotFinished'
        else:
            possible_endings = [
                StepType.BankBroke,
                StepType.PlayerGoesBankrupt,
                StepType.GameEndedManually
            ]
            for possible_ending in possible_endings:
                if possible_ending.name in self._df.type.tolist():
                    last_state['finished'] = possible_ending.name
            result = ast.literal_eval(self._df.result.iloc[-1])
            winner = max(result, key=result.get)
            last_state['result'] = result
            last_state['winner'] = winner
            self._df.drop('result', axis=1, inplace=True)
        return last_state

    def _run_minimal_verification(self) -> dict:
        # Run the minimal verification comparing final value of the players.
        result = dict(
            success=bool(),
            diffs=dict()
        )

        transcript_result = self._metadata['result']
        if not transcript_result:
            logger.info('Game not finished, cannot verify the results')
            result['success'] = False
            return result

        game_state_result = dict()
        for k, v in self._metadata['mapping'].items():
            try:
                value = self._df['{}_value'.format(v)].iloc[-1]
                game_state_result[v] = int(value)
            except KeyError:
                raise AttributeError('Player not found: {}'.format(v))

        checker = verification.StateVerification()
        result['success'] = checker.run(game_state_result, transcript_result)
        result['diffs'] = checker.diffs()
        return result

    def parse(self) -> dict:
        """Parses the transcript to a pandas Dataframe.

        During the parsing, the metadata will be written and saved together
        with the parsed transcript in the root folder of the raw transcript.
        Further, the game state results will be verified to the result of the
        transcript.

        Returns:
            The metadata of the parse result.

        Raises:
            FileNotFoundError: If transcript does not exist.
        """
        if not self._transcript:
            raise FileNotFoundError(
                'Transcript does not exist: {}'.format(self._transcript)
            )

        gtp = parsing.GameTranscriptProcessor(self._game)
        df_parsed = gtp.parse_transcript(self._transcript)
        tpp = parsing.TranscriptPostProcessor(df_parsed, self._game)
        df_processed = tpp.process()
        gsp = parsing.GameStateProcessor(df_processed, self._game)
        self._df = gsp.generate()

        mapping = self._anonymize_players()
        self._metadata['num_players'] = len(mapping.keys())
        self._metadata['mapping'] = mapping

        self._anonymize(self._df)
        self._metadata.update(self._anonymize(self._evaluate_last_state()))
        self._metadata['final_state'] = self._anonymize(gsp.final_state())

        self._metadata['verification'] = self._run_minimal_verification()

        self._metadata['unprocessed_lines'] = gtp.unprocessed_lines()

        _write_dataframe(dataframe_path(self._transcript), self._df)
        _write_json(metadata_path(self._transcript), self._metadata)

        return self._metadata


def dataframe_path(transcript: Path) -> Path:
    """Build the path to the parsed transcript.

    Args:
        transcript: The raw game transcript path.

    Returns:
        Path to the parsed transcript file.
    """
    return _build_path(transcript, '_final.csv')


def dataframe(transcript: Path) -> pd.DataFrame:
    """Loads the parsed transcript.

    Args:
        transcript: The raw game transcript path.

    Returns:
        The parsed transcript as pandas Dataframe.
    """
    file = dataframe_path(transcript)
    try:
        return _read_dataframe(file)
    except FileNotFoundError:
        logger.error('Parsed transcript not found: {}'.format(file))
        return pd.DataFrame()


def metadata_path(transcript: Path) -> Path:
    """Build the path to the game metadata.

    Args:
        transcript: The game transcript path.

    Returns:
        Path to the game metadata file.
    """
    return _build_path(transcript, '_metadata.json')


def metadata(transcript: Path) -> dict:
    """Loads the metadata of the parsed transcript.

    Args:
        transcript: The raw game transcript path.

    Returns:
        The metadata of the parsed transcript as dict.
    """
    file = metadata_path(transcript)
    try:
        return _read_json(file)
    except FileNotFoundError:
        logger.error('Metadata not found: {}'.format(file))
        return dict()


def transcript_name(name: str) -> str:
    """Extracts the transcript name from a filename.

    The transcript name consists of <game>_<id>.

    Args:
        name: The filename of the transcript.

    Returns:
        The identifier game name and id, separated by an underscore.
    """
    return '_'.join(name.split('_')[:2])


def transcript_id(name: str) -> str:
    """Extracts the transcript ID from a filename.

    Args:
        name: The filename of the transcript.

    Returns:
        The transcript id as string.
    """
    return name.split('_')[1]


def full_verification(transcript: Path) -> bool:
    """Run verification of the final state based on a ground truth file.

    It assumes that the ground truth file is saved in the same directory as
    the raw transcript, with `_truth.json` appended to the filename. E.g
    `1830_123456_truth.json`.

    Requires the raw transcript to be parsed and the metadata to be written.
    Extracts the final state from the metadata and prints the differences
    to the console.

    Args:
        transcript: The raw game transcript path.

    Returns:
        Success of the full verification.

    Raises:
        FileNotFoundError: If ground truth file was not found.
    """
    ground_truth = transcript.parent.joinpath(transcript.stem + '_truth.json')
    if not ground_truth.exists():
        raise FileNotFoundError(
            'Verification file not found: {}'.format(ground_truth)
        )

    transcript_metadata = metadata(transcript)
    final_state = transcript_metadata['final_state']
    mapping = transcript_metadata['mapping']
    for name, abbrev in mapping.items():
        final_state = _replace(final_state, abbrev, name)
        final_state.get('players')[name].pop('is_bankrupt')

    checker = verification.StateVerification()
    ret = checker.run(final_state, _read_json(ground_truth), out=True)
    return ret


def _build_path(transcript: Path, suffix: str) -> Path:
    # Builds the transcript path with its new suffix.
    return transcript.parent.joinpath(transcript.stem + suffix)


def _read_json(file: Path) -> dict:
    # Read a json file as dict.
    if not file.exists():
        raise FileNotFoundError(file)
    with open(file, 'r') as f:
        content = json.load(f)
    return content


def _read_dataframe(file: Path) -> pd.DataFrame:
    # Read the dataframe.
    if not file.exists():
        raise FileNotFoundError(file)
    return pd.read_csv(file, header=0, sep=',')


def _write_json(file: Path, content: dict) -> None:
    # Write a json file with indent of 2.
    with open(file, 'w') as f:
        f.write(json.dumps(content, indent=2))


def _write_dataframe(file: Path, df: pd.DataFrame) -> None:
    # Write dataframe to be opened by Excel (colon separator).
    df.to_csv(file, index=False, sep=',')


def _replace(obj, old, new):
    # Replaces the old with the new value in object.
    if isinstance(obj, dict):
        return {
            k.replace(old, new): _replace(v, old, new) for k, v in
            obj.items()
        }
    elif isinstance(obj, list):
        return [_replace(item, old, new) for item in obj]
    elif isinstance(obj, str):
        return obj.replace(old, new)
    elif isinstance(obj, pd.DataFrame):
        obj.replace(old, new, regex=False, inplace=True)  # full strings
        obj.columns = obj.columns.str.replace(old, new, regex=False)
        return obj
    else:
        return obj
