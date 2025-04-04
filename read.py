#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json

from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process game data from games from 18xx.games'
    )
    parser.add_argument(
        'data',
        type=Path,
        help='Path to the game data'
    )
    return parser.parse_args()


def main():
    with open(args.data, 'r') as f:
        data = json.load(f)
    actions = data['actions']
    action_types = set([a['type'] for a in actions])
    print(action_types)


if __name__ == '__main__':
    args = parse_arguments()
    main()
