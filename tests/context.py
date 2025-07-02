#!/usr/bin/env python

from pathlib import Path


def transcript_1830() -> Path:
    return _resources().joinpath('1830_201210.txt')


def transcript_1889() -> Path:
    return _resources().joinpath('1889_192767.txt')


def _resources() -> Path:
    return Path(__file__).parent.joinpath('resources')
