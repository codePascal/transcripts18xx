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
        """Parses the transcript to a pandas Dataframe."""
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
            The final states as dictionaries with keys `players` and
            `companies`.
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

    def save(self) -> None:
        """Saves the game data, its metadata and the final states.

        The files are saved in the transcript directory:
            - game data: `_final.csv`
            - metadata: `_metadata.json`
            - final states (anonymized): `_states.json`
        """
        _write_dataframe(dataframe(self._transcript), self._df)
        _write_json(metadata(self._transcript), self._game_info())
        _write_json(states(self._transcript), self.final_state(anonym=True))


def dataframe(transcript: Path) -> Path:
    """Build the path to the parsed transcript.

    Args:
        transcript: The game transcript path.

    Returns:
        Path to the parsed transcript file.

    Examples:
        >>> dataframe(Path('1830_123456.txt'))
        Path('1830_123456_final.csv')
    """
    return _build_path(transcript, '_final.csv')


def metadata(transcript: Path) -> Path:
    """Build the path to the game metadata.

    Args:
        transcript: The game transcript path.

    Returns:
        Path to the game metadata file.

    Examples:
        >>> metadata(Path('1830_123456.txt'))
        Path('1830_123456_metadata.json')
    """
    return _build_path(transcript, '_metadata.json')


def states(transcript: Path) -> Path:
    """Build the path to the final states.

    Args:
        transcript: The game transcript path.

    Returns:
        Path to the final states file.

    Examples:
        >>> states(Path('1830_123456.txt'))
        Path('1830_123456_states.json')
    """
    return _build_path(transcript, '_states.json')


def serialized(transcript: Path) -> Path:
    """Build the path to the serialized data.

    Args:
        transcript: The game transcript path.

    Returns:
        Path to the serialized data file.

    Examples:
        >>> serialized(Path('1830_123456.txt'))
        Path('1830_123456_serialized.json')
    """
    return _build_path(transcript, '_serialized.json')


def flattened(transcript: Path) -> Path:
    """Build the path to the flattened data.

    Args:
        transcript: The game transcript path.

    Returns:
        Path to the flattened data file.

    Examples:
        >>> dataframe(Path('1830_123456.txt'))
        Path('1830_123456_flattened.csv')
    """
    return _build_path(transcript, '_flattened.csv')


def serialize(transcript: Path) -> dict:
    """Serialize the game data to a json file.

    Each entry is represented by its index as the key and the row data as a
    dictionary to the index as value.

    Args:
        transcript: The path to the original transcript file.

    Returns:
        The serialized game data in a dictionary.
    """
    try:
        df = _read_dataframe(dataframe(transcript))
        result = df.to_dict(orient='index')
    except FileNotFoundError as e:
        print(e)
        return dict()
    _write_json(serialized(transcript), result)
    return result


def flatten(transcript: Path) -> pd.DataFrame:
    """Saves the game data as flatten structure.

    Opens up the states to represent each entry of the player and company states
    as a single column, e.g., "player1_cash". The columns representing the
    player and company states as dicts are dropped.

    Args:
        transcript: The path to the original transcript file.

    Returns:
        The flatten game data in a pandas Dataframe.
    """
    try:
        info = _read_json(metadata(transcript))
        players = list(info['players'].keys())
        game = games.Games.argparse('G{}'.format(info['game'])).select()
        df = _read_dataframe(dataframe(transcript))
        flat = df.apply(
            lambda x: _flatten_states(x, players, game.companies),
            axis=1,
            result_type='expand'
        )
        result = pd.concat([df, flat], axis=1)
        result.drop(players + list(game.companies), axis=1, inplace=True)
    except FileNotFoundError as e:
        print(e)
        return pd.DataFrame()
    except ValueError as e:
        print(e)
        return pd.DataFrame()
    _write_dataframe(flattened(transcript), result)
    return result


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


def _flatten_states(
        row: pd.Series, players: list[str], companies: list[str]) -> pd.Series:
    # Flatten the player and company states to a pandas Series.
    result = pd.Series()
    for p in sorted(players):
        player_state = parsing.engine.player.PlayerState.eval(row[p])
        result = pd.concat([result, player_state.flatten()])
    for c in sorted(companies):
        company_state = parsing.engine.company.CompanyState.eval(row[c])
        result = pd.concat([result, company_state.flatten()])
    return result
