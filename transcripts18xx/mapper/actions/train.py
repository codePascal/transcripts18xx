#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import enum


class TrainActions(enum.IntEnum):
    RunTrain = 0
    BuyTrain = 1
    PassTrain = 2
    SkipBuyTrain = 3
    SkipRunTrain = 4
    DiscardTrain = 5
    ExchangeTrain = 6
    ContributeTrain = 7


def actions(line: str) -> list:
    return [
        run_train(line),
        buy_train(line),
        pass_train(line),
        skip_buy_train(line),
        skip_run_train(line),
        discard_train(line),
        exchange_train(line),
        contribute_for_train(line)
    ]


def run_train(line: str) -> dict | None:
    match = re.search(r'(.*?) runs a (\w) train for \$(\d+): (.*)', line)
    if match:
        return dict(
            action=TrainActions.RunTrain.name,
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            route=match.group(4)
        )
    return None


def buy_train(line: str) -> dict | None:
    match = re.search(r'(.*?) buys a (\w+) train for \$(\d+) from (.*)', line)
    if match:
        return dict(
            action=TrainActions.BuyTrain.name,
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            source=match.group(4),
        )
    return None


def pass_train(line: str) -> dict | None:
    match = re.search(r'(.*?) passes buy trains', line)
    if match:
        return dict(
            action=TrainActions.PassTrain.name,
            company=match.group(1)
        )
    return None


def skip_buy_train(line: str) -> dict | None:
    match = re.search(r'(.*?) skips buy trains', line)
    if match:
        return dict(
            action=TrainActions.SkipBuyTrain.name,
            company=match.group(1),
        )
    return None


def skip_run_train(line: str) -> dict | None:
    match = re.search(r'(.*?) skips run routes', line)
    if match:
        return dict(
            action=TrainActions.SkipRunTrain.name,
            company=match.group(1),
        )
    return None


def discard_train(line: str) -> dict | None:
    match = re.search(r'(.*?) discards (\w+)', line)
    if match:
        return dict(
            action=TrainActions.DiscardTrain.name,
            company=match.group(1),
            train=match.group(2)
        )
    return None


def exchange_train(line: str) -> dict | None:
    match = re.search(
        r'(.*?) exchanges a (\d+) for a (\D) train for \$(\d+) from (.*)',
        line
    )
    if match:
        return dict(
            action=TrainActions.ExchangeTrain.name,
            company=match.group(1),
            old_train=match.group(2),
            new_train=match.group(3),
            amount=match.group(4),
            source=match.group(5)
        )
    return None


def contribute_for_train(line: str) -> dict | None:
    match = re.search(r'(.*?) contributes \$(\d+)', line)
    if match:
        return dict(
            action=TrainActions.ContributeTrain.name,
            player=match.group(1),
            amount=match.group(2)
        )
    return None
