#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


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
            action='TrainRan',
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
            action='TrainBought',
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
            action='TrainPassed',
            company=match.group(1)
        )
    return None


def skip_buy_train(line: str) -> dict | None:
    match = re.search(r'(.*?) skips buy trains', line)
    if match:
        return dict(
            action='TrainBuySkipped',
            company=match.group(1),
        )
    return None


def skip_run_train(line: str) -> dict | None:
    match = re.search(r'(.*?) skips run routes', line)
    if match:
        return dict(
            action='TrainRunSkipped',
            company=match.group(1),
        )
    return None


def discard_train(line: str) -> dict | None:
    match = re.search(r'(.*?) discards (\w+)', line)
    if match:
        return dict(
            action='TrainDiscarded',
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
            action='TrainExchanged',
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
            action='TrainBuyContributed',
            player=match.group(1),
            amount=match.group(2)
        )
    return None
