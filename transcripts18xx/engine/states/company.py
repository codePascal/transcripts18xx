#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Company state implementation

Module implements the company state and its maintainer.
"""
import ast
import json
import pandas as pd

from .state import State, States


class CompanyState(State):
    """CompanyState

    Class implements a company state object. The company is set up as IPO game
    style. That means if the company floats, it receives the full funds and
    shares can be brought from the IPO initially. There are other game styles,
    e.g. shares are in the company treasury. This class however, does not
    implement that! Further, it is assumed that the company is a 10-share
    company. A company has cash to fund its tile placements and trains, holds
    trains to generate revenue and has a president that holds the majority
    of the shares. A company has a share price as well.

    Args:
        name: The name of the company.
        trains: The available trains and amount of each train.

    Attributes:
        trains: The available trains and amount of each train.
        ipo: Number of shares available in the IPO.
        market: Number of shares available on the market.
        president: The name of the player which is president of that company.
        share_price: The market share price.
    """

    def __init__(self, name: str, trains: dict):
        super().__init__(name)

        self.trains = trains.copy()
        self.ipo = 10  # assume IPO and market game style
        self.market = 0
        self.president = None
        self.share_price = 0

    def __eq__(self, other):
        return (
                self.name == other.name and
                self.cash == other.cash and
                self.privates == other.privates and
                self.trains == other.trains and
                self.ipo == other.ipo and
                self.market == other.market and
                self.president == other.president and
                self.share_price == other.share_price
        )

    @staticmethod
    def eval(rep: str):
        st = CompanyState(name=str(), trains={})
        if isinstance(rep, str):
            rep = ast.literal_eval(rep)
        st.__dict__ = rep
        return st

    def flatten(self) -> pd.Series:
        """Creates a series from the state representation.

        The trains dictionary is expanded to single indexes with the train type
        appended, e.g. `company1_trains_2`.

        Returns:
            A pandas Series with the members of the state and their values.
        """
        key = f'{self.name}_%s'
        data = {
            key % 'cash': self.cash,
            key % 'privates': json.dumps(self.privates),
            key % 'ipo': self.ipo,
            key % 'market': self.market,
            key % 'president': self.president,
            key % 'share_price': self.share_price
        }
        for k, v in self.trains.items():
            data[key % 'trains_' + k] = v
        return pd.Series(data)

    @staticmethod
    def _proc_train(train):
        if train == 'D':
            return train
        return str(int(train))

    def receives_dividend(self, per_share: int) -> None:
        self.cash += self.market * per_share

    def withholds(self, amount: int):
        self.cash += amount

    def is_pared(self, share_price: int):
        self.share_price = share_price

    def lays_tile(self, amount: int):
        self.cash -= amount

    def places_token(self, amount: int):
        self.cash -= amount

    def buys_train(self, train: str, amount: int):
        self.trains[self._proc_train(train)] += 1
        self.cash -= amount

    def discards_train(self, train: str):
        self.trains[self._proc_train(train)] -= 1

    def exchanges_train(self, old_train: str, new_train: str, amount: int):
        self.discards_train(old_train)
        self.buys_train(new_train, amount)

    def receives_funds(self, amount: int):
        self.cash += amount

    def share_price_moves(self, share_price: int):
        self.share_price = share_price

    def president_assignment(self, player: str):
        self.president = player

    def trains_rust(self, train: str):
        self.trains[self._proc_train(train)] = 0

    def sells_share(self, num_shares: int, source: str):
        if source == 'market':
            self.market -= num_shares
        elif source == 'IPO':
            self.ipo -= num_shares
        else:
            raise ValueError(f'Source not available: {source}')

    def receives_share(self, num_shares: int):
        self.market += num_shares

    def sells_train(self, train: str, amount: int):
        self.discards_train(train)
        self.cash += amount


class Companies(States):
    """Companies

    Class implements a maintainer class for all companies in the game.

    Args:
        names: The names of the companies.
        trains: The available trains in the game.

    Attributes:
        states: The states of type `CompanyState`.
    """

    def __init__(self, names: list[str], trains: list[str]):
        super().__init__()

        trains = {k: 0 for k in sorted(trains)}
        self.states = [CompanyState(n, trains) for n in names]

    def share_prices(self) -> dict:
        """Creates view of the share prices of all companies.

        Returns:
            Dict containing the company names and their share prices.
        """
        return {st.name: st.share_price for st in self.states}
