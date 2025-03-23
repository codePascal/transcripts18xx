#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from pathlib import Path

from transcripts18xx.preprocessing import GameTranscriptProcessor
from transcripts18xx.postprocessing import TranscriptPostProcessor
from transcripts18xx.games import selector


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process transcripts from games from 18xx.games'
    )
    parser.add_argument(
        'game',
        type=selector.Games.argparse,
        choices=list(selector.Games),
        help='Game name of transcript, e.g. G1830',
    )
    parser.add_argument(
        'transcript',
        type=Path,
        help='Path to the game transcript'
    )
    return parser.parse_args()


def main():
    game = selector.select_game(args.game)
    if not args.transcript.exists():
        sys.exit('Transcript does not exist: {}'.format(args.transcript))

    gtp = GameTranscriptProcessor(args.transcript, game)
    gtp.parse_transcript()
    df = gtp.save_to_dataframe()

    tpp = TranscriptPostProcessor(df)


if __name__ == '__main__':
    args = parse_arguments()
    main()
