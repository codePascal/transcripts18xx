#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Event matching and processing.

Module implements engine step handlers for events appearing during the game.
This events can be triggered by player or company actions or by another event.
"""
import re
import abc
import pandas as pd

from ..states.player import Players, PlayerState
from ..states.company import Companies, CompanyState
from .step import EngineStep, StepType, StepParent


class EventStep(EngineStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.parent = StepParent.Event


class ReceiveShare(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives a (\d+)% share of (.*)')
        self.type = StepType.ReceiveShare

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke(
            PlayerState.receives_share,
            dict(
                company=row.company,
                num_shares=int(0.1 * row.percentage),
            ),
            row.player
        )
        companies.invoke(
            CompanyState.sells_share,
            dict(
                num_shares=int(0.1 * row.percentage),
                source='IPO'  # Assume from IPO
            ),
            row.company
        )


class ReceiveFunds(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives \$(\d+)')
        self.type = StepType.ReceiveFunds

        self._dismiss = ['sells']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.receives_funds,
            dict(amount=row.amount),
            row.company
        )


class CompanyFloats(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) floats')
        self.type = StepType.CompanyFloats

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class SelectsHome(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) must choose city for token')
        self.type = StepType.SelectsHome

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class DoesNotRun(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) does not run')
        self.type = StepType.DoesNotRun

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class SharePriceMove(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r"(.*?)'s share price moves (.*?) from \$(\d+) to \$(\d+)"
        )
        self.type = StepType.SharePriceMoves

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            direction=match.group(2),
            share_price=match.group(4)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.share_price_moves,
            dict(share_price=row.share_price),
            row.company
        )


class NewPhase(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Phase (\w+) \(')
        self.type = StepType.NewPhase

    def _process_match(self, line: str, match) -> dict:
        return dict(
            phase=match.group(1)
        )


class BankBroke(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- The bank has broken --')
        self.type = StepType.BankBroke

    def _process_match(self, line: str, match) -> dict:
        return dict()


class GameOver(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Game over:')
        self.type = StepType.GameOver

    def _process_match(self, line: str, match) -> dict:
        # TODO: process rankings, and add ranking to separate column key
        return dict()


class OperatingRound(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Operating Round (\d+\.\d+)')
        self.type = StepType.OperatingRound

    def _process_match(self, line: str, match) -> dict:
        return dict(
            sequence='OR {}'.format(match.group(1))
        )


class StockRound(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Stock Round (\d+)')
        self.type = StepType.StockRound

    def _process_match(self, line: str, match) -> dict:
        return dict(
            sequence='SR {}'.format(match.group(1))
        )


class PresidentNomination(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) becomes the president of (.*)')
        self.type = StepType.PresidentNomination

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.president_assignment,
            dict(player=row.player),
            row.company
        )


class PriorityDeal(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) has priority deal')
        self.type = StepType.PriorityDeal

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        # First set all to False, the invoke specific player.
        players.invoke_all(
            PlayerState.has_priority_deal, dict(priority_deal=False),
        )
        players.invoke(
            PlayerState.has_priority_deal, dict(priority_deal=True), row.player
        )


class OperatesCompany(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) operates (.*)')
        self.type = StepType.OperatesCompany

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2)
        )


class AllPrivatesClose(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: Private companies close')
        self.type = StepType.AllPrivatesClose

    def _process_match(self, line: str, match) -> dict:
        return dict()

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke_all(PlayerState.private_closes, dict())
        companies.invoke_all(CompanyState.private_closes, dict())


class PrivateCloses(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) closes')
        self.type = StepType.PrivateCloses

    def _process_match(self, line: str, match) -> dict:
        return dict(
            private=match.group(1)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(private=row.private)
        players.invoke_all(PlayerState.private_closes, args)
        companies.invoke_all(CompanyState.private_closes, args)


class PrivateAuctioned(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) goes up for auction')
        self.type = StepType.PrivateAuctioned

    def _process_match(self, line: str, match) -> dict:
        return dict(
            private=match.group(1)
        )


class TrainsRust(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: (\d+) trains rust')
        self.type = StepType.TrainsRust

    def _process_match(self, line: str, match) -> dict:
        return dict(
            train=match.group(1)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke_all(CompanyState.trains_rust, dict(train=row.train))


class PlayerGoesBankrupt(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'-- (\w+) goes bankrupt and sells remaining shares --'
        )
        self.type = StepType.PlayerGoesBankrupt

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke(PlayerState.goes_bankrupt, dict(), row.player)
