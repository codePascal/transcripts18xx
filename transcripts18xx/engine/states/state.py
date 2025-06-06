#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic state implementation.

Module implements abstract base class process and maintain states of the game.
"""
import ast
import json

import pandas as pd


class State(object):
    """State

    Class implements a state of a game object, e.g., player or company.

    Args:
        name: The name of the state object.

    Attributes:
        name: The name of the state object.
        cash: The available cash.
        privates: The privates the object has and their values.
    """

    def __init__(self, name: str):
        self.name = name

        self.cash = 0
        self.privates = dict()

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
        key = '{}_%s'.format(self.name)
        data = {
            key % 'cash': self.cash,
            key % 'privates': json.dumps(self.privates)
        }
        return pd.Series(data)

    def update(self, *args):
        pass

    def collects(self, amount: int) -> None:
        self.cash += amount

    def buys_private(self, private: str, amount: int, value: int) -> None:
        self.privates[private] = value
        self.cash -= amount

    def private_closes(self, private: str = None) -> None:
        if private is None:
            self.privates = dict()
        elif private in self.privates:
            self.privates.pop(private)


class States(object):
    """States

    Class implements a base class to maintain all states of a given type, e.g.,
    all players or all companies.

    Attributes:
        states: The states of type `State`.
    """

    def __init__(self):
        self.states = list()

    def __repr__(self):
        return '\n'.join([st.__repr__() for st in self.states]) + '\n'

    def update(self, args: dict) -> None:
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
        return {st.name: ast.literal_eval(st.__repr__()) for st in self.states}
