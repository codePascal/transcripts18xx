#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Event matching and processing.

Module implements pattern handlers for events appearing during the game. This
events can be triggered by player or company actions or by another event.
"""
import re
import abc

from .pattern import PatternHandler, PatternType, PatternParent


class Events(PatternType):
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


class EventHandler(PatternHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.parent = PatternParent.Event


class ReceiveShare(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives a (\d+)% share of (.*)')
        self.type = Events.ReceiveShare

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3)
        )


class ReceiveFunds(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives \$(\d+)')
        self.type = Events.ReceiveFunds

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2)
        )


class CompanyFloats(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) floats')
        self.type = Events.CompanyFloats

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class SelectsHome(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) must choose city for token')
        self.type = Events.SelectsHome

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class DoesNotRun(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) does not run')
        self.type = Events.DoesNotRun

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1)
        )


class SharePriceMove(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r"(.*?)'s share price moves (.*?) from \$(\d+) to \$(\d+)"
        )
        self.type = Events.SharePriceMoves

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            direction=match.group(2),
            share_price=match.group(4)
        )


class NewPhase(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Phase (\w+) \(')
        self.type = Events.NewPhase

    def _handle(self, line: str, match) -> dict:
        return dict(
            phase=match.group(1)
        )


class BankBroke(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- The bank has broken --')
        self.type = Events.BankBroke

    def _handle(self, line: str, match) -> dict:
        return dict()


class GameOver(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Game over:')
        self.type = Events.GameOver

    def _handle(self, line: str, match) -> dict:
        return dict()


class OperatingRound(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Operating Round (\d+\.\d+)')
        self.type = Events.OperatingRound

    def _handle(self, line: str, match) -> dict:
        return dict(
            round='OR {}'.format(match.group(1))
        )


class StockRound(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Stock Round (\d+)')
        self.type = Events.StockRound

    def _handle(self, line: str, match) -> dict:
        return dict(
            round='SR {}'.format(match.group(1))
        )


class PresidentNomination(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) becomes the president of (.*)')
        self.type = Events.PresidentNomination

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2)
        )


class PriorityDeal(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) has priority deal')
        self.type = Events.PriorityDeal

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1)
        )


class OperatesCompany(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) operates (.*)')
        self.type = Events.OperatesCompany

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2)
        )


class AllPrivatesClose(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: Private companies close')
        self.type = Events.AllPrivatesClose

    def _handle(self, line: str, match) -> dict:
        return dict()


class PrivateCloses(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) closes')
        self.type = Events.PrivateCloses

    def _handle(self, line: str, match) -> dict:
        return dict(
            private=match.group(1)
        )


class PrivateAuctioned(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) goes up for auction')
        self.type = Events.PrivateAuctioned

    def _handle(self, line: str, match) -> dict:
        return dict(
            private=match.group(1)
        )


class TrainsRust(EventHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: (\d+) trains rust')
        self.type = Events.TrainsRust

    def _handle(self, line: str, match) -> dict:
        return dict(
            train=match.group(1)
        )
