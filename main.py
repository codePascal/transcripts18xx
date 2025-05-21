#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to parse and process a game transcript from 18xx.games.

Features
--------
* Parses a transcript file for a specified 18xx game (e.g. 1830, 1889).
* Verifies that the game state at the end of the transcript is valid.
* Optionally serializes the parsed game into a JSON-compatible Python dict.
* Optionally flattens the game data into a Pandas DataFrame for analysis.

Usage
-----
$ python main.py G1830 transcript.txt [--skip-verify] [--serialize] [--flatten]

Args
----
* game              The game identifier used to select game rules.
* transcript        Path to the text file containing the transcript.
* --skip-verify     Skips final game state verification.
* --serialize       Saves the parsed game data as a JSON dict.
* --flatten         Flattens the game into a Pandas DataFrame and prints it.
"""
import argparse

from pathlib import Path

from transcripts18xx import transcript


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process a game transcript from 18xx.games'
    )
    parser.add_argument(
        'game',
        type=transcript.games.Games.argparse,
        choices=transcript.games.Games,
        help='Game type of transcript, e.g. G1830',
    )
    parser.add_argument(
        'transcript',
        type=Path,
        help='Path to the game transcript'
    )
    parser.add_argument(
        '--skip-verify',
        action='store_true',
        help='Skip the verification of the final state'
    )
    parser.add_argument(
        '--serialize',
        action='store_true',
        help='Serialize the game data into a json dict'
    )
    parser.add_argument(
        '--flatten',
        action='store_true',
        help='Flatten the game data into a pandas Dataframe'
    )
    return parser.parse_args()


def main(args):
    game = args.game.select()
    if not args.transcript.exists():
        print('Transcript does not exist: {}'.format(args.transcript))
        return
    parser = transcript.TranscriptParser(args.transcript, game)
    parser.parse()
    parser.save()
    if not args.skip_verify:
        parser.verify_result(minimal=False)
    if args.flatten:
        transcript.flatten(args.transcript)
    if args.serialize:
        transcript.serialize(args.transcript)


if __name__ == '__main__':
    main(parse_arguments())
