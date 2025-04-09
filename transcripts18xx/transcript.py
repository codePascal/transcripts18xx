#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Transcript processing pipeline

Module implements the transcript processing pipeline with parsing the
transcript, processing the result and mapping player and company states.
"""
import pandas as pd

from pathlib import Path

from .processing.preprocessing import GameTranscriptProcessor
from .processing.postprocessing import TranscriptPostProcessor
from .games import Game18xx


def parse(transcript: Path, game: Game18xx) -> pd.DataFrame:
    """Parses the transcript to a pandas Dataframe.

    Args:
        transcript: The transcript path.
        game: The game type of the transcript.

    Returns:
        The parsed data in a pandas Dataframe.
    """
    gtp = GameTranscriptProcessor(transcript)
    gtp.parse_transcript()
    df = gtp.save_to_dataframe()

    tpp = TranscriptPostProcessor(df, game)
    tpp.process()
    df = tpp.save_to_dataframe(transcript)

    return df
