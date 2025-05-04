#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from pathlib import Path

from transcripts18xx import transcript


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process transcripts from games from 18xx.games'
    )
    parser.add_argument(
        'game',
        type=transcript.games.Games.argparse,
        choices=transcript.games.Games,
        help='Game type of transcripts, e.g. G1830',
    )
    parser.add_argument(
        '--skip-verify',
        action='store_true',
        help='Skip the verification of the final states'
    )
    return parser.parse_args()


def main():
    game = args.game.select()
    if isinstance(game, transcript.games.Game1830):
        transcripts = Path(
            'C:/Users/mup01/git/18xx/records18xx/transcripts/1830'
        )
    else:
        print('Game not implemented: {}'.format(args.game))
        return
    transcripts = [
        file for file in transcripts.iterdir() if file.suffix == '.txt'
    ]
    for file in transcripts:
        print('### Parsing {} ###'.format(file))
        parser = transcript.TranscriptParser(file, game)
        parser.parse()
        parser.save()
        parser.serialize()
        if not args.skip_verify:
            parser.verify_result()


if __name__ == '__main__':
    args = parse_arguments()
    main()
