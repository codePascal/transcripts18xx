#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

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
        help='Game type of transcripts, e.g. G1830',
    )
    return parser.parse_args()


def main():
    game = args.game.select()
    if isinstance(game, games.Game1830):
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
        transcript.parse(file, game)


if __name__ == '__main__':
    args = parse_arguments()
    main()
