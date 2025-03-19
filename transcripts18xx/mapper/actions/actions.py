#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import common, company, player


def actions(line: str) -> list:
    return common_actions(line) + company_actions(line) + player_actions(line)


def common_actions(line: str) -> list:
    return [
        common.receives(line),
        common.buys(line),
        common.collects(line),
        common.passes(line)
    ]


def company_actions(line: str) -> list:
    return [
        company.places_token(line),
        company.skips_token(line),
        company.lays_tile(line),
        company.skips_tile(line),
        company.runs_train(line),
        company.skips_run_train(line),
        company.skips_buy_private(line),
        company.pays_dividend(line)
    ]


def player_actions(line: str) -> list:
    return [
        player.bids(line),
        player.operates_company(line),
        player.pars_company(line),
        player.declines_sell_shares(line)
    ]
