#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


def main():
    game = args.game.select()
    if not args.transcript.exists():
        print('Transcript does not exist: {}'.format(args.transcript))
        return
    parser = transcript.TranscriptParser(args.transcript, game)
    parser.parse()
    parser.save()
    parser.serialize()
    if not args.skip_verify:
        parser.verify_result(minimal=False)


if __name__ == '__main__':
    args = parse_arguments()
    main()
