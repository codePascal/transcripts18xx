#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

from pathlib import Path

from transcripts18xx.preprocessing import GameTranscriptProcessor
from transcripts18xx.postprocessing import TranscriptPostProcessor
from transcripts18xx.games import Games


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process transcripts from games from 18xx.games'
    )
    parser.add_argument(
        'game',
        type=Games.argparse,
        choices=list(Games),
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

    gtp = GameTranscriptProcessor(args.transcript)
    gtp.parse_transcript()
    df = gtp.save_to_dataframe()

    tpp = TranscriptPostProcessor(df, game)
    tpp.process()
    df = gtp.save_to_dataframe()


if __name__ == '__main__':
    args = parse_arguments()
    main()
