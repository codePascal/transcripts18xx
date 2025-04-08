#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path


def transcript_1817() -> Path:
    return _resources().joinpath('1817_200348.txt')


def transcript_1830() -> Path:
    return _resources().joinpath('1830_201210.txt')


def parsed_transcript_1830() -> Path:
    return _resources().joinpath('1830_201210_parsed.csv')


def processed_transcript_1830() -> Path:
    return _resources().joinpath('1830_201210_processed.csv')


def _resources() -> Path:
    return Path(__file__).parent.joinpath('resources')
