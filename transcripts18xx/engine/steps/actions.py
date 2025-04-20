#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Action matching and processing.

Module implements engine step handlers for actions performed by a player or a
company during the game.
"""
import re
import abc
import pandas as pd

from ..states.player import Players, PlayerState
from ..states.company import Companies, CompanyState
from .step import EngineStep, StepType, StepParent


class Actions(StepType):
    """Actions

    Enum class describing the actions performed by a player or a company.
    """
    PayOut = 0
    Withhold = 1
    BuyShare = 2
    SellShares = 3
    Par = 5
    Bid = 6
    Pass = 7
    Skip = 8
    Collect = 9
    BuyPrivate = 10
    LayTile = 11
    PlaceToken = 12
    BuyTrain = 13
    RunTrain = 14
    DiscardTrain = 15
    ExchangeTrain = 16
    Contribute = 17


class ActionStep(EngineStep, abc.ABC):
    """ActionStep

    Class implements engine steps that are actions by companies or player.
    """

    def __init__(self):
        super().__init__()
        self.parent = StepParent.Action


class PayOut(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) pays out \$(\d+) = \$(\d+) per share')
        self.type = Actions.PayOut

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2),
            per_share=match.group(3)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke_all(
            PlayerState.receives_dividend,
            dict(company=row.company, per_share=row.per_share)
        )
        companies.invoke(
            CompanyState.receives_dividend,
            dict(per_share=row.per_share),
            row.company
        )


class Withhold(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) withholds \$(\d+)')
        self.type = Actions.Withhold

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.withholds,
            dict(amount=row.amount),
            row.company
        )


class BuyShare(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) buys a (\d+)% share of (.*?) from the (.*?) for \$(\d+)'
        )
        self.type = Actions.BuyShare

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3),
            source=match.group(4),
            amount=match.group(5)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke(
            PlayerState.buys_shares,
            dict(
                company=row.company,
                num_shares=int(0.1 * row.percentage),
                amount=row.amount,
            ),
            row.player
        )
        companies.invoke(
            CompanyState.sells_share,
            dict(
                num_shares=int(0.1 * row.percentage),
                source=row.source
            ),
            row.company
        )


class SellShare(ActionStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.SellShares

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            percentage='{}{}'.format(match.group(2), '0'),
            company=match.group(3),
            amount=match.group(4)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke(
            PlayerState.sells_shares,
            dict(
                company=row.company,
                num_shares=int(0.1 * row.percentage),
                amount=row.amount
            ),
            row.player
        )
        companies.invoke(
            CompanyState.receives_share,
            dict(num_shares=int(0.1 * row.percentage)),
            row.company
        )


class SellSingleShare(SellShare):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) sells a (\d+)0% share of (.*?) and receives \$(\d+)'
        )


class SellMultipleShares(SellShare):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) sells (\d+) shares of (.*?) and receives \$(\d+)'
        )


class Pass(ActionStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.Pass

    def _process_match(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
        )


class NoValidActions(Pass):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) has no valid actions and passes')


class RegularPass(Pass):

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

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes buy companies')


class PassAuction(Pass):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes on (.*)')


class PassTile(Pass):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes lay/upgrade track')


class PassToken(Pass):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes place a token')


class PassBuyTrain(Pass):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) passes buy trains')


class Skip(ActionStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.Skip

    def _process_match(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
        )


class DeclineSellShare(Skip):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) declines to sell shares')


class DeclineBuyShare(Skip):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) declines to buy shares')


class SkipBuyPrivate(Skip):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips buy companies')


class SkipLayTile(Skip):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips lay track')


class SkipPlaceToken(Skip):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips place a token')


class SkipBuyTrain(Skip):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips buy trains')


class SkipRunTrain(Skip):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) skips run routes')


class ParCompany(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) pars (.*?) at \$(\d+)')
        self.type = Actions.Par

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2),
            share_price=match.group(3)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.is_pared,
            dict(share_price=row.share_price),
            row.company
        )


class Bid(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) bids \$(\d+) for (.*)')
        self.type = Actions.Bid

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            amount=match.group(2),
            private=match.group(3),
        )


class Collect(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) collects \$(\d+) from (.*)')
        self.type = Actions.Collect

    def _process_match(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
            amount=match.group(2),
            source=match.group(3),
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(
            amount=row.amount
        )
        if not pd.isna(row.player):
            players.invoke(PlayerState.collects, args, row.player)
        else:
            companies.invoke(CompanyState.collects, args, row.company)


class BuyPrivate(ActionStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.BuyPrivate

    def _process_match(self, line: str, match) -> dict:
        raise NotImplementedError

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        args = dict(
            private=row.private, amount=row.amount, value=privates[row.private]
        )
        if not pd.isna(row.player):
            # Player buys from Auction.
            players.invoke(PlayerState.buys_private, args, row.player)
        else:
            # Company buys from player.
            companies.invoke(CompanyState.buys_private, args, row.company)
            players.invoke(PlayerState.sells_private, args, row.source)


class BuyPrivateFromPlayer(BuyPrivate):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) buys (.*?) from (.*?) for \$(\d+)')

        self._dismiss = ['share', 'train']
        self._required = ['from']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
            private=match.group(2),
            source=match.group(3),
            amount=match.group(4)
        )


class BuyPrivateFromAuction(BuyPrivate):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) buys (.*?) for \$(\d+)')

        self._dismiss = ['share', 'train', 'from']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
            private=match.group(2),
            amount=match.group(3),
            source='Auction',
        )


class WinAuctionAgainst(BuyPrivate):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) wins the auction for (.*?) with a bid of \$(\d+)'
        )

        self._dismiss = ['share', 'train', 'from']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
            private=match.group(2),
            amount=match.group(3),
            source='Auction',
        )


class WinAuction(BuyPrivate):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) wins the auction for (.*?) with the only bid of \$(\d+)'
        )

        self._dismiss = ['share', 'train', 'from']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
            private=match.group(2),
            amount=match.group(3),
            source='Auction',
        )


class LayTile(ActionStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.LayTile

    def _process_match(self, line: str, match) -> dict:
        raise NotImplementedError

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.lays_tile,
            dict(amount=row.amount),
            row.company
        )


class LayTileForMoney(LayTile):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) spends \$(\d+) and lays tile #(.*?) with rotation (\d+) on '
            r'(.*)'
        )

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2),
            tile=match.group(3),
            rotation=match.group(4),
            location=match.group(5)
        )


class LayTileForFree(LayTile):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) lays tile #(.*?) with rotation (\d+) on (.*)'
        )

        self._dismiss = ['spends']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            tile=match.group(2),
            rotation=match.group(3),
            location=match.group(4),
            amount='0'
        )


class PlaceToken(ActionStep, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.PlaceToken

    def _process_match(self, line: str, match) -> dict:
        raise NotImplementedError

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.places_token,
            dict(amount=row.amount),
            row.company
        )


class PlaceTokenForMoney(PlaceToken):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) places a token on (.*) for \$(\d+)')

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            location=match.group(2),
            amount=match.group(3)
        )


class PlaceTokenForFree(PlaceToken):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) places a token on (.*)')

        self._dismiss = ['for']

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            location=match.group(2),
            amount='0'
        )


class BuyTrain(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) buys a (\w+) train for \$(\d+) from (.*)'
        )
        self.type = Actions.BuyTrain

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            source=match.group(4),
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.buys_train,
            dict(train=row.train, amount=row.amount),
            row.company
        )
        if row.source in [c.name for c in companies.states]:
            companies.invoke(
                CompanyState.sells_train,
                dict(train=row.train, amount=row.amount),
                row.source
            )


class RunTrain(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) runs a (\w) train for \$(\d+): (.*)')
        self.type = Actions.RunTrain

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            route=match.group(4)
        )


class DiscardTrain(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) discards (\w+)')
        self.type = Actions.DiscardTrain

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            train=match.group(2)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.discards_train,
            dict(train=row.train),
            row.company
        )


class ExchangeTrain(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) exchanges a (\d+) for a (\D) train for \$(\d+) from (.*)'
        )
        self.type = Actions.ExchangeTrain

    def _process_match(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            old_train=match.group(2),
            new_train=match.group(3),
            amount=match.group(4),
            source=match.group(5)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        companies.invoke(
            CompanyState.exchanges_train,
            dict(
                old_train=row.old_train,
                new_train=row.new_train,
                amount=row.amount
            ),
            row.company
        )


class Contribute(ActionStep):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) contributes \$(\d+)')
        self.type = Actions.Contribute

    def _process_match(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            amount=match.group(2)
        )

    def _update(self, row: pd.Series, players: Players, companies: Companies,
                privates: dict) -> None:
        players.invoke(
            PlayerState.contributes,
            dict(amount=row.amount),
            row.player
        )
        # Select the company that has not much money and requires a train
        companies_require_train = [
            c.name for c in companies.states
            if c.president == row.player and sum(c.trains.values()) == 0
        ]
        if len(companies_require_train) != 1:
            raise AttributeError(
                'Target for contribution unknown:\n{}'.format(row.to_string())
            )
        companies.invoke(
            CompanyState.collects,
            dict(amount=row.amount),
            companies_require_train[0]
        )
