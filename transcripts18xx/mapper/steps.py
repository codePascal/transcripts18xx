#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum

from actions import actions
from events import events


def search(name: str) -> enum.Enum:
    print(actions.train.TrainActions)

    return actions.train.TrainActions.BuyTrain
