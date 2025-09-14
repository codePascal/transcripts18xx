#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Event matching and processing

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
    """EventStep
    """

    def __init__(self):
        super().__init__()
        self.parent = StepParent.Event


class ReceiveShare(EventStep):
    """ReceiveShare
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives a (\d+)% share of (.*)')
        self.type = StepType.ReceiveShare

    def _process_match(self, line: str, match) -> dict:
        return {
            'player': match.group(1),
            'percentage': match.group(2),
            'company': match.group(3)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        num_shares = int(0.1 * row.percentage)
        players.invoke(
            PlayerState.receives_share,
            {'company': row.company, 'num_shares': num_shares},
            row.player
        )
        companies.invoke(
            CompanyState.sells_share,
            {'num_shares': num_shares, 'source': 'IPO'},
            row.company
        )


class ReceiveFunds(EventStep):
    """ReceiveFunds
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) receives \$(\d+)')
        self.type = StepType.ReceiveFunds

        self._dismiss = ['sells']

    def _process_match(self, line: str, match) -> dict:
        return {'company': match.group(1), 'amount': match.group(2)}

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.receives_funds,
            {'amount': row.amount},
            row.company
        )


class CompanyFloats(EventStep):
    """CompanyFloats
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) floats')
        self.type = StepType.CompanyFloats

    def _process_match(self, line: str, match) -> dict:
        return {'company': match.group(1)}


class SelectsHome(EventStep):
    """SelectsHome
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) must choose city for (home )?token')
        self.type = StepType.SelectsHome

    def _process_match(self, line: str, match) -> dict:
        return {'company': match.group(1)}


class DoesNotRun(EventStep):
    """DoesNotRun
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) does not run')
        self.type = StepType.DoesNotRun

    def _process_match(self, line: str, match) -> dict:
        return {'company': match.group(1)}


class SharePriceMove(EventStep):
    """SharePriceMove
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r"(.*?)'s share price moves (.*?) from \$(\d+) to \$(\d+)"
        )
        self.type = StepType.SharePriceMoves

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'direction': match.group(2),
            'share_price': match.group(4)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.share_price_moves,
            {'share_price': row.share_price},
            row.company
        )


class NewPhase(EventStep):
    """NewPhase
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Phase (\w+) \(')
        self.type = StepType.NewPhase

    def _process_match(self, line: str, match) -> dict:
        return {'phase': match.group(1)}


class BankBroke(EventStep):
    """BankBroke
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- The bank has broken --')
        self.type = StepType.BankBroke

    def _process_match(self, line: str, match) -> dict:
        return {}


class GameOver(EventStep):
    """GameOver
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Game over: (.*) --')
        self.type = StepType.GameOver

    def _process_match(self, line: str, match) -> dict:
        # Match everything up to the next comma
        pattern = re.compile(r'([^,]+?)\s+\(\$(\d+)\)')
        matches = re.findall(pattern, match.group(1))
        result = {p.strip(): int(v) for p, v in matches}
        return {'result': str(result)}


class OperatingRound(EventStep):
    """OperatingRound
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Operating Round (\d+\.\d+)')
        self.type = StepType.OperatingRound

    def _process_match(self, line: str, match) -> dict:
        return {'sequence': f'OR {match.group(1)}'}


class StockRound(EventStep):
    """StockRound
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Stock Round (\d+)')
        self.type = StepType.StockRound

    def _process_match(self, line: str, match) -> dict:
        return {'sequence': f'SR {match.group(1)}'}


class PresidentNomination(EventStep):
    """PresidentNomination
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) becomes the president of (.*)')
        self.type = StepType.PresidentNomination

    def _process_match(self, line: str, match) -> dict:
        return {'player': match.group(1), 'company': match.group(2)}

    def _update(self, row: pd.Series, players: Players,
                companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.president_assignment,
            {'player': row.player},
            row.company
        )


class PriorityDeal(EventStep):
    """PriorityDeal
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) has priority deal')
        self.type = StepType.PriorityDeal

    def _process_match(self, line: str, match) -> dict:
        return {'player': match.group(1)}

    def _update(self, row: pd.Series, players: Players,
                companies: Companies,
                privates: dict) -> None:
        # First set all to False, the invoke specific player.
        players.invoke_all(
            PlayerState.has_priority_deal, {'priority_deal': False},
        )
        players.invoke(
            PlayerState.has_priority_deal, {'priority_deal': True},
            row.player
        )


class OperatesCompany(EventStep):
    """OperatesCompany
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) operates (.*)')
        self.type = StepType.OperatesCompany

    def _process_match(self, line: str, match) -> dict:
        return {'player': match.group(1), 'company': match.group(2)}


class AllPrivatesClose(EventStep):
    """AllPrivatesClose
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: Private companies close')
        self.type = StepType.AllPrivatesClose

    def _process_match(self, line: str, match) -> dict:
        return {}

    def _update(self, row: pd.Series, players: Players,
                companies: Companies,
                privates: dict) -> None:
        players.invoke_all(PlayerState.private_closes, {})
        companies.invoke_all(CompanyState.private_closes, {})


class PrivateCloses(EventStep):
    """PrivateCloses
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) closes')
        self.type = StepType.PrivateCloses

    def _process_match(self, line: str, match) -> dict:
        return {'private': match.group(1)}

    def _update(self, row: pd.Series, players: Players,
                companies: Companies,
                privates: dict) -> None:
        args = {'private': row.private}
        players.invoke_all(PlayerState.private_closes, args)
        companies.invoke_all(CompanyState.private_closes, args)


class PrivateAuctioned(EventStep):
    """PrivateAuctioned
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) goes up for auction')
        self.type = StepType.PrivateAuctioned

    def _process_match(self, line: str, match) -> dict:
        return {'private': match.group(1)}


class TrainsRust(EventStep):
    """TrainsRust
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- Event: (\d+) trains rust')
        self.type = StepType.TrainsRust

    def _process_match(self, line: str, match) -> dict:
        return {'train': match.group(1)}

    def _update(self, row: pd.Series, players: Players,
                companies: Companies,
                privates: dict) -> None:
        companies.invoke_all(CompanyState.trains_rust, {'train': row.train})


class PlayerGoesBankrupt(EventStep):
    """PlayerGoesBankrupt
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'-- (.*?) goes bankrupt and sells remaining shares --'
        )
        self.type = StepType.PlayerGoesBankrupt

    def _process_match(self, line: str, match) -> dict:
        return {'player': match.group(1)}

    def _update(self, row: pd.Series, players: Players,
                companies: Companies,
                privates: dict) -> None:
        players.invoke(PlayerState.goes_bankrupt, {}, row.player)


class GameEndedManually(EventStep):
    """"GameEndedManually
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'Game ended manually by (.*?)')
        self.type = StepType.GameEndedManually

    def _process_match(self, line: str, match) -> dict:
        return {}


class ConfirmedConsent(EventStep):
    """ConfirmedConsent
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'^(.*?): \u2022 confirmed receiving consent from (.*)'
        )
        self.type = StepType.ConfirmedConsent

    def _process_match(self, line: str, match) -> dict:
        return {}


class MasterMode(EventStep):
    """MasterMode
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'\u2022 Action\((.*?)\) via Master Mode by: (.*)'
        )
        self.type = StepType.MasterMode

    def _process_match(self, line: str, match) -> dict:
        return {}


class DateEntry(EventStep):
    """DateEntry
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'-- \b\d{4}-\d{2}-\d{2}\b --')
        self.type = StepType.DateEntry

    def _process_match(self, line: str, match) -> dict:
        return {}
