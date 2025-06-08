#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to parse and process a game transcript from 18xx.games.

Features
--------
* Parses a transcript file for a specified 18xx game (e.g. 1830, 1889).
* Optionally runs full verification of the final game state based on a ground
truth file.

Usage
-----
$ python main.py G1830 transcript.txt [--skip-verify]

Args
----
* game              The game identifier used to select game rules.
* transcript        Path to the text file containing the transcript.
* --skip-verify     Skips final game state verification.
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
    return parser.parse_args()


def main(args):
    game = args.game.select()
    if not args.transcript.exists():
        print('Transcript does not exist: {}'.format(args.transcript))
        return
    parser = transcript.TranscriptParser(args.transcript, game)
    parser.parse()
    if not args.skip_verify:
        transcript.full_verification(args.transcript)


if __name__ == '__main__':
    main(parse_arguments())
