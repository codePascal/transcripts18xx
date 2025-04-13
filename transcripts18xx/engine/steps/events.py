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


# TODO: add player goes bankrupt:
#  `-- (JuicyBerry) goes bankrupt and sells remaining shares --`

class Events(StepType):
    """Events

    Enum class describing the events appearing during the game.
    """
    ReceiveShare = 0
    ReceiveFunds = 1
    CompanyFloats = 2
    SelectsHome = 3
    DoesNotRun = 4
    SharePriceMoves = 5
    NewPhase = 6
    BankBroke = 7
    GameOver = 8
    OperatingRound = 9
    StockRound = 10
    PresidentNomination = 11
    PriorityDeal = 12
    OperatesCompany = 13
    AllPrivatesClose = 14
    PrivateCloses = 15
    PrivateAuctioned = 16
    TrainsRust = 17


class EventStep(EngineStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.parent = StepParent.Event


class ReceiveShare(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives a (\d+)% share of (.*)')
        self.type = Events.ReceiveShare

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(
            company=row.company,
            num_shares=int(0.1 * row.percentage),
        )
        players.invoke(PlayerState.receives_share, args, row.player)


class ReceiveFunds(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives \$(\d+)')
        self.type = Events.ReceiveFunds

        self._dismiss = ['sells']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(amount=row.amount)
        companies.invoke(CompanyState.receives_funds, args, row.company)


class CompanyFloats(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) floats')
        self.type = Events.CompanyFloats

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class SelectsHome(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) must choose city for token')
        self.type = Events.SelectsHome

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class DoesNotRun(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) does not run')
        self.type = Events.DoesNotRun

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
        self.type = Events.SharePriceMoves

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            direction=match.group(2),
            share_price=match.group(4)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(share_price=row.share_price)
        companies.invoke(CompanyState.share_price_moves, args, row.company)


class NewPhase(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Phase (\w+) \(')
        self.type = Events.NewPhase

    def _process_match(self, line: str, match) -> dict:
        return dict(
            phase=match.group(1)
        )


class BankBroke(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- The bank has broken --')
        self.type = Events.BankBroke

    def _process_match(self, line: str, match) -> dict:
        return dict()


class GameOver(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Game over:')
        self.type = Events.GameOver

    def _process_match(self, line: str, match) -> dict:
        return dict()


class OperatingRound(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Operating Round (\d+\.\d+)')
        self.type = Events.OperatingRound

    def _process_match(self, line: str, match) -> dict:
        return dict(
            round='OR {}'.format(match.group(1))
        )


class StockRound(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Stock Round (\d+)')
        self.type = Events.StockRound

    def _process_match(self, line: str, match) -> dict:
        return dict(
            round='SR {}'.format(match.group(1))
        )


class PresidentNomination(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) becomes the president of (.*)')
        self.type = Events.PresidentNomination

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(player=row.player)
        companies.invoke(CompanyState.president_assignment, args, row.company)


class PriorityDeal(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) has priority deal')
        self.type = Events.PriorityDeal

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict()
        players.invoke(PlayerState.has_priority_deal, args, row.player)


class OperatesCompany(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) operates (.*)')
        self.type = Events.OperatesCompany

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2)
        )


class AllPrivatesClose(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: Private companies close')
        self.type = Events.AllPrivatesClose

    def _process_match(self, line: str, match) -> dict:
        return dict()

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict()
        players.invoke_all(PlayerState.private_closes, args)
        companies.invoke_all(CompanyState.private_closes, args)


class PrivateCloses(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) closes')
        self.type = Events.PrivateCloses

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
        self.type = Events.PrivateAuctioned

    def _process_match(self, line: str, match) -> dict:
        return dict(
            private=match.group(1)
        )


class TrainsRust(EventStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: (\d+) trains rust')
        self.type = Events.TrainsRust

    def _process_match(self, line: str, match) -> dict:
        return dict(
            train=match.group(1)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(train=row.train)
        companies.invoke_all(CompanyState.trains_rust, args)
