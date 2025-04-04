#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import abc

from .pattern import PatternHandler, PatternType, PatternParent


class Actions(PatternType):
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


class ActionHandler(PatternHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.parent = PatternParent.Action


class PayOut(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) pays out \$(\d+) = \$(\d+) per share')
        self.type = Actions.PayOut

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2),
            per_share=match.group(3)
        )


class Withhold(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) withholds \$(\d+)')
        self.type = Actions.Withhold

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            amount=match.group(2)
        )


class BuyShare(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) buys a (\d+)% share of (.*?) from the (.*?) for \$(\d+)'
        )
        self.type = Actions.BuyShare

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            percentage=match.group(2),
            company=match.group(3),
            source=match.group(4),
            amount=match.group(5)
        )


class SellShare(ActionHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.SellShares

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            percentage='{}{}'.format(match.group(2), '0'),
            company=match.group(3),
            amount=match.group(4)
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


class Pass(ActionHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.Pass

    def _handle(self, line: str, match) -> dict:
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
            'has no valid actions and passes',
            'passes buy companies',
            'passes on',
            'passes lay/upgrade track',
            'passes place a token',
            'passes buy trains'
        ]

    def _handle(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1)
        )


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


class Skip(ActionHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.Skip

    def _handle(self, line: str, match) -> dict:
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


class ParCompany(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) pars (.*?) at \$(\d+)')
        self.type = Actions.Par

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            company=match.group(2),
            amount=match.group(3)
        )


class Bid(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) bids \$(\d+) for (.*)')
        self.type = Actions.Bid

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            amount=match.group(2),
            private=match.group(3),
        )


class Collect(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) collects \$(\d+) from (.*)')
        self.type = Actions.Collect

    def _handle(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
            amount=match.group(2),
            source=match.group(3),
        )


class BuyPrivate(ActionHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.BuyPrivate


class BuyPrivateFromPlayer(BuyPrivate):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) buys (.*?) from (.*?) for \$(\d+)')

        self._dismiss = ['share', 'train']
        self._required = ['from']

    def _handle(self, line: str, match) -> dict:
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

    def _handle(self, line: str, match) -> dict:
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

    def _handle(self, line: str, match) -> dict:
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

    def _handle(self, line: str, match) -> dict:
        return dict(
            entity=match.group(1),
            private=match.group(2),
            amount=match.group(3),
            source='Auction',
        )


class LayTile(ActionHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.LayTile


class LayTileForMoney(LayTile):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) spends \$(\d+) and lays tile #(.*?) with rotation (\d+) on '
            r'(.*)'
        )

    def _handle(self, line: str, match) -> dict:
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

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            tile=match.group(2),
            rotation=match.group(3),
            location=match.group(4),
            amount='0'
        )


class PlaceToken(ActionHandler, abc.ABC):

    def __init__(self):
        super().__init__()
        self.type = Actions.PlaceToken


class PlaceTokenForMoney(PlaceToken):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) places a token on (.*) for \$(\d+)')

    def _handle(self, line: str, match) -> dict:
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

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            location=match.group(2),
            amount='0'
        )


class BuyTrain(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) buys a (\w+) train for \$(\d+) from (.*)'
        )
        self.type = Actions.BuyTrain

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            source=match.group(4),
        )


class RunTrain(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) runs a (\w) train for \$(\d+): (.*)')
        self.type = Actions.RunTrain

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            train=match.group(2),
            amount=match.group(3),
            route=match.group(4)
        )


class DiscardTrain(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) discards (\w+)')
        self.type = Actions.DiscardTrain

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            train=match.group(2)
        )


class ExchangeTrain(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(
            r'(.*?) exchanges a (\d+) for a (\D) train for \$(\d+) from (.*)'
        )
        self.type = Actions.ExchangeTrain

    def _handle(self, line: str, match) -> dict:
        return dict(
            company=match.group(1),
            old_train=match.group(2),
            new_train=match.group(3),
            amount=match.group(4),
            source=match.group(5)
        )


class Contribute(ActionHandler):

    def __init__(self):
        super().__init__()
        self.pattern = re.compile(r'(.*?) contributes \$(\d+)')
        self.type = Actions.Contribute

    def _handle(self, line: str, match) -> dict:
        return dict(
            player=match.group(1),
            amount=match.group(2)
        )
