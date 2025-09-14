#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic state implementation.

Module implements an abstract base class to process and maintain states of the
game.
"""
import ast
import json

import pandas as pd


class State:
    """State

    Class implements a state of a game object, e.g., player or company. In 18xx
    games a company or a player have cash available and can hold private
    companies.

    Args:
        name: The name of the state object, i.e. player or company name.

    Attributes:
        name: The name of the state object.
        cash: The available cash.
        privates: The privates the object has and their values.
    """

    def __init__(self, name: str):
        self.name = name

        self.cash = 0
        self.privates = {}

    def __repr__(self):
        return self.__dict__.__str__()

    def __eq__(self, other):
        return (
                self.name == other.name and
                self.cash == other.cash and
                self.privates == other.privates
        )

    @staticmethod
    def eval(rep: str | dict):
        """Construct a State object from its string representation.

        Args:
            rep: The output from __repr__() as string or evaluated as dict.

        Returns:
            State object.
        """
        st = State(name=str())
        if isinstance(rep, str):
            rep = ast.literal_eval(rep)
        st.__dict__ = rep
        return st

    def flatten(self) -> pd.Series:
        """Creates a series from the state representation.

        Returns:
            A pandas Series with the members of the state and their values.
        """
        key = f'{self.name}_%s'
        data = {
            key % 'cash': self.cash,
            key % 'privates': json.dumps(self.privates)
        }
        return pd.Series(data)

    def update(self, *args, **kwargs) -> None:
        """Update the current state.

        Args:
            *args: The arguments required for the update.
        """
        return

    def collects(self, amount: int) -> None:
        """Collects money from e.g. a private.

        Args:
            amount: Amount collected.
        """
        self.cash += amount

    def buys_private(self, private: str, amount: int, value: int) -> None:
        """Buys private from auction, other player or company.

        Args:
            private: The private which is bought.
            amount: The amount payed for the private.
            value: The value of the private.
        """
        self.privates[private] = value
        self.cash -= amount

    def private_closes(self, private: str = None) -> None:
        """All or one private close.

        Args:
            private: The name of the private that closes. If None, all privates
                will be closed, i.e., removed from the state.
        """
        if private is None:
            self.privates = {}
        elif private in self.privates:
            self.privates.pop(private)


class States:
    """States

    Class implements a base class to maintain all states of a given type, e.g.,
    all players or all companies.

    Attributes:
        states: The states of type `State`.
    """

    def __init__(self):
        self.states = []

    def __repr__(self):
        return '\n'.join([st.__repr__() for st in self.states]) + '\n'

    def update(self, args: dict) -> None:
        """Invoke updating of individual states.

        Args:
            args: The arguments required for the update.
        """
        for st in self.states:
            st.update(**args)

    def get(self, name: str) -> State:
        """Get a state by its name.

        Args:
            name: The name of the state.

        Returns:
            The state object.
        """
        return next((st for st in self.states if st.name == name))

    def invoke(self, func, args, name) -> None:
        """Invoke a function of a state.

        Args:
            func: The function to invoke.
            args: The arguments for the function call as dict.
            name: The name of the state to invoke.
        """
        if name in [st.name for st in self.states]:
            func(self.get(name), **args)

    def invoke_all(self, func, args) -> None:
        """Invoke a function on all states.

        Args:
            func: The function to invoke.
            args: The arguments of the function call as dict.
        """
        for st in self.states:
            self.invoke(func, args, st.name)

    def as_dict(self) -> dict:
        """Represents the states as dict, with names as keys."""
        return {st.name: ast.literal_eval(repr(st)) for st in self.states}
