#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Player state implementation

Module implements a player state and maintainer class.
"""

from .state import State, States


class PlayerState(State):
    """PlayerState

    Class implements a player state object.

    Args:
        name: The name of the player.
        initial_cash: The initial cash.
        shares: The available companies and the number of shares the player
            has in the beginning (which is zero obviously).

    Attributes:
        name: The name of the player.
        cash: The available cash of the player.
        privates: The privates the player has and their values.
        value: The value of the player, i.e., the cash, the shares and privates.
        shares: The company shares the player holds.
        priority_deal: Whether the player has priority in the next SR.
    """

    def __init__(self, name: str, initial_cash: int, shares: dict):
        super().__init__(name)

        self.cash = initial_cash
        self.value = initial_cash
        self.shares = shares.copy()
        self.priority_deal = False

    def __eq__(self, other):
        return (
                self.name == other.name and
                self.cash == other.cash and
                self.privates == other.privates and
                self.value == other.value and
                self.shares == other.shares and
                self.priority_deal == other.priority_deal
        )

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

    def buys_shares(self, company: str, num_shares: int, amount: int) -> None:
        self.shares[company] += num_shares
        self.cash -= amount

    def sells_shares(self, company: str, num_shares: int,
                     amount: int) -> None:
        self.shares[company] -= num_shares
        self.cash += amount

    def sells_private(self, private: str, amount: int, value: int):
        self.privates.pop(private)
        self.cash += amount

    def contributes(self, amount: int):
        self.cash -= amount

    def receives_share(self, company: str, num_shares: int):
        self.shares[company] += num_shares

    def has_priority_deal(self, priority_deal: bool):
        self.priority_deal = priority_deal

    def goes_bankrupt(self):
        self.cash = 0


class Players(States):
    """Players

    Class implements a maintainer class for all players in the game.

    Args:
        names: The names of the players.
        companies: The available companies in the game.
        initial_cash: The initial cash that is divided by the players.

    Attributes:
        states: The states of type `Player`.
    """

    def __init__(self, names: list[str], companies: list[str],
                 initial_cash: int):
        super().__init__()

        initial_value = int(initial_cash / len(names))
        shares = {k: 0 for k in sorted(companies)}
        self.states = [PlayerState(n, initial_value, shares) for n in names]
