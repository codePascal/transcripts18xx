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
* --debug           Enable debug output in logger.
"""
import argparse
import json
import logging

from pathlib import Path

import transcripts18xx as trx


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process a game transcript from 18xx.games'
    )
    parser.add_argument(
        'game',
        type=trx.Games.argparse,
        choices=trx.Games,
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
        '--debug',
        action='store_true',
        help='Enable debug output of logger'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('main.log', mode='w'),
            logging.StreamHandler()
        ]
    )

    game = args.game.select()
    parser = trx.TranscriptParser(args.transcript, game)
    result = parser.parse()
    print(json.dumps(result, indent=2))
    if not args.skip_verify:
        trx.full_verification(args.transcript)


if __name__ == '__main__':
    main()
