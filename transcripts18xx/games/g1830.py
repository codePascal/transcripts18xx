#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..mapper.actions import bid, buy, receive, par, passes, collect,operates
from ..mapper.events import privates, trains, rounds, player, company
from .pattern import GamePattern


class Game1830(GamePattern):

    def __init__(self):
        super().__init__()

    def _check_events(self, line: str) -> dict | None:
        return self._match(
            [
                privates.close(line),
                privates.is_auctioned(line),
                rounds.phase_change(line),
                rounds.operating_round(line),
                rounds.stock_round(line),
                rounds.game_over(line),
                trains.rust(line),
                player.becomes_president(line),
                player.has_priority_deal(line),
                company.floats(line)
            ]
        )

    def _check_actions(self, line: str) -> dict | None:
        return self._match(
            [
                bid.bid(line),
                buy.buy(line),
                collect.collect(line),
                par.par(line),
                receive.receive(line),
                passes.passes(line),
                operates.operates(line)
            ]
        )

    def extract_pattern(self, line: str) -> dict | None:
        return self._match(
            [
                self._check_events(line),
                self._check_actions(line)
            ]
        )
