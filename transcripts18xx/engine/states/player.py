#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Player state implementation

Module implements a player state and maintainer class.
"""
import ast
import pandas as pd
import json

from .state import State, States


class PlayerState(State):
    """PlayerState

    Class implements a player state object. In 18xx games, a player has its
    cash to spend, can hold shares of different companies, can have priority
    deal in the next stock round and has an associated value based on its cash,
    public company shares and private companies.

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
        is_bankrupt: Flag to denote that player is bankrupt.
    """

    def __init__(self, name: str, initial_cash: int, shares: dict):
        super().__init__(name)

        self.cash = initial_cash
        self.value = initial_cash
        self.shares = shares.copy()
        self.priority_deal = False

        self.is_bankrupt = False

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
        if isinstance(rep, str):
            rep = ast.literal_eval(rep)
        st.__dict__ = rep
        return st

    def flatten(self) -> pd.Series:
        """Creates a series from the state representation.

        The shares dictionary is expanded to single indexes with the company
        name appended, e.g. `player1_shares_company1`.

        Returns:
            A pandas Series with the members of the state and their values.
        """
        key = '{}_%s'.format(self.name)
        data = {
            key % 'cash': self.cash,
            key % 'privates': json.dumps(self.privates),
            key % 'value': self.value,
            key % 'priority_deal': self.priority_deal
        }
        for k, v in self.shares.items():
            data[key % 'shares_' + k] = v
        return pd.Series(data)

    def update(self, share_prices: dict) -> None:
        """Update the player value.

        The player values consists of the cash, the number of shares a player
        holds with their share price and the values of the privates.

        Args:
            share_prices: The share price of each company.
        """
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
        if not self.is_bankrupt:
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
        self.is_bankrupt = True

    def exchanges_private_for_share(self, private: str, num_shares: int,
                                    company: str) -> None:
        self.privates.pop(private)
        self.shares[company] += num_shares


class Players(States):
    """Players

    Class implements a maintainer class for all players in the game.

    Args:
        names: The names of the players.
        companies: The available companies in the game.
        initial_cash: The initial cash that is divided by the players.

    Attributes:
        states: The states of type `PlayerState`.
    """

    def __init__(self, names: list[str], companies: list[str],
                 initial_cash: int):
        super().__init__()

        initial_value = int(initial_cash / len(names))
        shares = {k: 0 for k in sorted(companies)}
        self.states = [PlayerState(n, initial_value, shares) for n in names]
