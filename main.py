#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from pathlib import Path

from transcripts18xx import transcript, games


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process transcripts from games from 18xx.games'
    )
    parser.add_argument(
        'game',
        type=games.Games.argparse,
        choices=list(games.Games),
        help='Game name of transcript, e.g. G1830',
    )
    parser.add_argument(
        'transcript',
        type=Path,
        help='Path to the game transcript'
    )
    return parser.parse_args()


def main():
    game = args.game.select()
    if not args.transcript.exists():
        sys.exit('Transcript does not exist: {}'.format(args.transcript))
    df = transcript.parse(args.transcript, game)
    print(df)


if __name__ == '__main__':
    args = parse_arguments()
    main()
