#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

from .state import State, States


class PlayerState(State):

    def __init__(self, name: str, initial_cash: int, shares: dict):
        super().__init__(name)

        self.cash = initial_cash
        self.value = initial_cash
        self.shares = shares
        self.priority_deal = False

    @staticmethod
    def eval(rep: str):
        st = PlayerState(name=str(), initial_cash=int(), shares=dict())
        st.__dict__ = eval(rep)
        return st

    def update(self, share_prices: dict):
        self.value = self.cash
        self.value += sum(self.shares[c] * v for c, v in share_prices.items())
        self.value += sum(self.privates.values())

    def receives_dividend(self, company: str, per_share: int) -> None:
        self.cash += self.shares[company] * per_share

    def buys_shares(self, company: str, num_shares: int,
                    amount: int) -> None:
        self.shares[company] += num_shares
        self.cash -= amount

    def sells_shares(self, company: str, num_shares: int,
                     amount: int) -> None:
        self.shares[company] -= num_shares
        self.cash += amount

    def sells_private(self, private: str, amount: int):
        self.privates.pop(private)
        self.cash += amount

    def contributes(self, amount: int):
        self.cash -= amount

    def receives_share(self, company: str, num_shares: int):
        self.shares[company] += num_shares

    def has_priority_deal(self):
        self.priority_deal = True


class Players(States):

    def __init__(self, names: list[str], companies: list[str],
                 initial_cash: int):
        super().__init__()

        initial_value = int(initial_cash / len(names))
        shares = {k: 0 for k in companies}
        self.states = [PlayerState(n, initial_value, shares) for n in names]
