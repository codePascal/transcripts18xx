#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Action matching and processing

Module implements engine step handlers for actions performed by a player or a
company during the game.
"""
import re
import abc
import pandas as pd

from ..states.player import Players, PlayerState
from ..states.company import Companies, CompanyState
from .step import EngineStep, StepType, StepParent


class ActionStep(EngineStep, abc.ABC):
    """ActionStep
    """

    def __init__(self):
        super().__init__()
        self.parent = StepParent.Action


class PayOut(ActionStep):
    """PayOut
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) pays out \$(\d+) = \$(\d+) per share')
        self.type = StepType.PayOut

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'amount': match.group(2),
            'per_share': match.group(3)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke_all(
            PlayerState.receives_dividend,
            {'company': row.company, 'per_share': row.per_share}
        )
        companies.invoke(
            CompanyState.receives_dividend,
            {'per_share': row.per_share},
            row.company
        )


class Withhold(ActionStep):
    """Withhold
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) withholds \$(\d+)')
        self.type = StepType.Withhold

    def _process_match(self, line: str, match) -> dict:
        return {'company': match.group(1), 'amount': match.group(2)}

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.withholds, {'amount': row.amount}, row.company
        )


class BuyShare(ActionStep):
    """BuyShare
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) buys a (\d+)% share of (.*?) from the (.*?) for \$(\d+)'
        )
        self.type = StepType.BuyShare

    def _process_match(self, line: str, match) -> dict:
        return {
            'player': match.group(1),
            'percentage': match.group(2),
            'company': match.group(3),
            'source': match.group(4),
            'amount': match.group(5)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        num_shares = int(0.1 * row.percentage)
        players.invoke(
            PlayerState.buys_shares,
            {
                'company': row.company,
                'num_shares': num_shares,
                'amount': row.amount
            },
            row.player
        )
        companies.invoke(
            CompanyState.sells_share,
            {'num_shares': num_shares, 'source': row.source},
            row.company
        )


class SellShare(ActionStep, abc.ABC):
    """SellShare
    """

    def __init__(self):
        super().__init__()
        self.type = StepType.SellShares

    def _process_match(self, line: str, match) -> dict:
        return {
            'player': match.group(1),
            'percentage': f'{match.group(2)}0',
            'company': match.group(3),
            'amount': match.group(4)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        num_shares = int(0.1 * row.percentage)
        players.invoke(
            PlayerState.sells_shares,
            {
                'company': row.company,
                'num_shares': num_shares,
                'amount': row.amount
            },
            row.player
        )
        companies.invoke(
            CompanyState.receives_share, {'num_shares': num_shares}, row.company
        )


class SellSingleShare(SellShare):
    """SellSingleShare
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) sells a (\d+)0% share of (.*?) and receives \$(\d+)'
        )


class SellMultipleShares(SellShare):
    """SellMultipleShares
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) sells (\d+) shares of (.*?) and receives \$(\d+)'
        )


class Pass(ActionStep, abc.ABC):
    """Pass
    """

    def __init__(self):
        super().__init__()
        self.type = StepType.Pass

    def _process_match(self, line: str, match) -> dict:
        return {'entity': match.group(1)}


class NoValidActions(Pass):
    """NoValidActions
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) has no valid actions and passes')


class RegularPass(Pass):
    """RegularPass
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes')  # search is different

        self._dismiss = [
            'actions',  # has no valid actions and passes
            'buy',  # passes buy companies
            'on',  # passes on private
            'track',  # passes lay/upgrade track
            'token',  # passes place a token
            'trains'  # passes buy trains
        ]


class PassBuyPrivate(Pass):
    """PassBuyPrivate
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes buy companies')


class PassAuction(Pass):
    """PassAuction
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes on (.*)')


class PassTile(Pass):
    """PassTile
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes lay/upgrade track')


class PassToken(Pass):
    """PassToken
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes place a token')


class PassBuyTrain(Pass):
    """PassBuyTrain
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes buy trains')


class Skip(ActionStep, abc.ABC):
    """Skip
    """

    def __init__(self):
        super().__init__()
        self.type = StepType.Skip

    def _process_match(self, line: str, match) -> dict:
        return {'entity': match.group(1)}


class DeclineSellShare(Skip):
    """DeclineSellShare
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) declines to sell shares')


class DeclineBuyShare(Skip):
    """DeclineBuyShare
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) declines to buy shares')


class DeclinePlaceToken(Skip):
    """DeclinePlaceToken
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) declines to place token')


class SkipBuyPrivate(Skip):
    """SkipBuyPrivate
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips buy companies')


class SkipLayTile(Skip):
    """SkipLayTile
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips lay track')


class SkipPlaceToken(Skip):
    """SkipPlaceToken
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips place a token')


class SkipBuyTrain(Skip):
    """SkipBuyTrain
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips buy trains')


class SkipRunTrain(Skip):
    """SkipRunTrain
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips run routes')


class ParCompany(ActionStep):
    """ParCompany
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) pars (.*?) at \$(\d+)')
        self.type = StepType.Par

    def _process_match(self, line: str, match) -> dict:
        return {
            'player': match.group(1),
            'company': match.group(2),
            'share_price': match.group(3)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.is_pared,
            {'share_price': row.share_price},
            row.company
        )


class Bid(ActionStep):
    """Bid
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) bids \$(\d+) for (.*)')
        self.type = StepType.Bid

    def _process_match(self, line: str, match) -> dict:
        return {
            'player': match.group(1),
            'amount': match.group(2),
            'private': match.group(3)
        }


class Collect(ActionStep):
    """Collect
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) collects \$(\d+) from (.*)')
        self.type = StepType.Collect

    def _process_match(self, line: str, match) -> dict:
        return {
            'entity': match.group(1),
            'amount': match.group(2),
            'source': match.group(3)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = {'amount': row.amount}
        if not pd.isna(row.player):
            players.invoke(PlayerState.collects, args, row.player)
        else:
            companies.invoke(CompanyState.collects, args, row.company)


class BuyPrivate(ActionStep, abc.ABC):
    """BuyPrivate
    """

    def __init__(self):
        super().__init__()
        self.type = StepType.BuyPrivate

    def _process_match(self, line: str, match) -> dict:
        raise NotImplementedError

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = {
            'private': row.private,
            'amount': row.amount,
            'value': privates[row.private]
        }
        if not pd.isna(row.player):
            # Player buys from Auction.
            players.invoke(PlayerState.buys_private, args, row.player)
        else:
            # Company buys from player.
            companies.invoke(CompanyState.buys_private, args, row.company)
            players.invoke(PlayerState.sells_private, args, row.source)


class BuyPrivateFromPlayer(BuyPrivate):
    """BuyPrivateFromPlayer
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) buys (.*?) from (.*?) for \$(\d+)')

        self._dismiss = ['share', 'train']
        self._required = ['from']

    def _process_match(self, line: str, match) -> dict:
        return {
            'entity': match.group(1),
            'private': match.group(2),
            'source': match.group(3),
            'amount': match.group(4)
        }


class BuyPrivateFromAuction(BuyPrivate):
    """BuyPrivateFromAuction
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) buys (.*?) for \$(\d+)')

        self._dismiss = ['share', 'train', 'from']

    def _process_match(self, line: str, match) -> dict:
        return {
            'entity': match.group(1),
            'private': match.group(2),
            'amount': match.group(3),
            'source': 'Auction'
        }


class WinAuctionAgainst(BuyPrivate):
    """WinAuctionAgainst
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) wins the auction for (.*?) with a bid of \$(\d+)'
        )

        self._dismiss = ['share', 'train', 'from']

    def _process_match(self, line: str, match) -> dict:
        return {
            'entity': match.group(1),
            'private': match.group(2),
            'amount': match.group(3),
            'source': 'Auction'
        }


class WinAuction(BuyPrivate):
    """WinAuction
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) wins the auction for (.*?) with the only bid of \$(\d+)'
        )

        self._dismiss = ['share', 'train', 'from']

    def _process_match(self, line: str, match) -> dict:
        return {
            'entity': match.group(1),
            'private': match.group(2),
            'amount': match.group(3),
            'source': 'Auction'
        }


class LayTile(ActionStep, abc.ABC):
    """LayTile
    """

    def __init__(self):
        super().__init__()
        self.type = StepType.LayTile

    def _process_match(self, line: str, match) -> dict:
        raise NotImplementedError

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.lays_tile, {'amount': row.amount}, row.company
        )


class LayTileForMoney(LayTile):
    """LayTileForMoney
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) spends \$(\d+) and lays tile #(.*?) with rotation (\d+) on '
            r'(.*)'
        )

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'amount': match.group(2),
            'tile': match.group(3),
            'rotation': match.group(4),
            'location': match.group(5)
        }


class LayTileForFree(LayTile):
    """LayTileForFree
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) lays tile #(.*?) with rotation (\d+) on (.*)'
        )

        self._dismiss = ['spends']

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'tile': match.group(2),
            'rotation': match.group(3),
            'location': match.group(4),
            'amount': '0'
        }


class PlaceToken(ActionStep, abc.ABC):
    """PlaceToken
    """

    def __init__(self):
        super().__init__()
        self.type = StepType.PlaceToken

    def _process_match(self, line: str, match) -> dict:
        raise NotImplementedError

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.places_token, {'amount': row.amount}, row.company
        )


class PlaceTokenForMoney(PlaceToken):
    """PlaceTokenForMoney
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) places a token on (.*) for \$(\d+)')

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'location': match.group(2),
            'amount': match.group(3),
        }


class PlaceTokenForFree(PlaceToken):
    """PlaceTokenForFree
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) places a token on (.*)')

        self._dismiss = ['for']

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'location': match.group(2),
            'amount': '0',
        }


class BuyTrain(ActionStep):
    """BuyTrain
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) buys a (\w+) train for \$(\d+) from (.*)'
        )
        self.type = StepType.BuyTrain

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'train': match.group(2),
            'amount': match.group(3),
            'source': match.group(4)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = {'train': row.train, 'amount': row.amount}
        companies.invoke(CompanyState.buys_train, args, row.company)
        if row.source in [c.name for c in companies.states]:
            companies.invoke(CompanyState.sells_train, args, row.source)


class RunTrain(ActionStep):
    """RunTrain
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) runs a (\w) train for \$(\d+): (.*)')
        self.type = StepType.RunTrain

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'train': match.group(2),
            'amount': match.group(3),
            'route': match.group(4)
        }


class DiscardTrain(ActionStep):
    """DiscardTrain
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) discards (\w+)')
        self.type = StepType.DiscardTrain

    def _process_match(self, line: str, match) -> dict:
        return {'company': match.group(1), 'train': match.group(2)}

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.discards_train, {'train': row.train}, row.company
        )


class ExchangeTrain(ActionStep):
    """ExchangeTrain
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) exchanges a (\d+) for a (\D) train for \$(\d+) from (.*)'
        )
        self.type = StepType.ExchangeTrain

    def _process_match(self, line: str, match) -> dict:
        return {
            'company': match.group(1),
            'old_train': match.group(2),
            'new_train': match.group(3),
            'amount': match.group(4),
            'source': match.group(5),
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.exchanges_train,
            {
                'old_train': row.old_train,
                'new_train': row.new_train,
                'amount': row.amount
            },
            row.company
        )


class Contribute(ActionStep):
    """Contribute
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) contributes \$(\d+)')
        self.type = StepType.Contribute

    def _process_match(self, line: str, match) -> dict:
        return {
            'player': match.group(1),
            'amount': match.group(2),
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke(
            PlayerState.contributes, {'amount': row.amount}, row.player
        )
        companies.invoke(
            CompanyState.collects, {'amount': row.amount}, row.company
        )


class ExchangePrivate(ActionStep):
    """ExchangePrivate
    """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) exchanges (.*?) from the (\w+) for a (\d+)0% share of (.*)'
        )
        self.type = StepType.ExchangePrivate

    def _process_match(self, line: str, match) -> dict:
        return {
            'player': match.group(1),
            'private': match.group(2),
            'source': match.group(3),
            'percentage': f'{match.group(4)}0',
            'company': match.group(5)
        }

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        num_shares = int(0.1 * row.percentage)
        players.invoke(
            PlayerState.exchanges_private_for_share,
            {
                'private': row.private,
                'num_shares': num_shares,
                'company': row.company
            },
            row.player
        )
        companies.invoke(
            CompanyState.sells_share,
            {'num_shares': num_shares, 'source': row.source},
            row.company
        )
