#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Company state implementation

Module implements the company state and its maintainer.
"""
from .state import State, States


class CompanyState(State):

    def __init__(self, name: str, trains: dict):
        super().__init__(name)

        self.trains = trains
        self.ipo = 10  # assume IPO and market game style
        self.market = 0
        self.president = None
        self.share_price = 0

    @staticmethod
    def _proc_train(train):
        if train == 'D':
            return train
        else:
            return str(int(train))

    def receives_dividend(self, company: str, per_share: int) -> None:
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


class Companies(States):

    def __init__(self, names: list[str], trains: list[str]):
        super().__init__()

        trains = {k: 0 for k in trains}
        self.states = [CompanyState(n, trains) for n in names]

    def share_prices(self) -> dict:
        return {st.name: st.share_price for st in self.states}
