#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic state implementation.

Module implements abstract base class process and maintain states of the game.
"""


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
        attrs = ', '.join(f'{k}={repr(v)}' for k, v in self.__dict__.items())
        return f'{self.__class__.__name__}({attrs})'

    def update(self, *args):
        pass

    def receives_dividend(self, company: str, per_share: int) -> None:
        raise NotImplementedError

    def collects(self, amount: int) -> None:
        self.cash += amount

    def buys_private(self, private: str, amount: int, value: int):
        self.privates[private] = value
        self.cash -= amount

    def private_closes(self, private: str = None):
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

    def update(self, args: dict):
        for st in self.states:
            st.update(**args)

    def get(self, name: str) -> State:
        return next((st for st in self.states if st.name == name))

    def invoke(self, func, args, name):
        if name in [st.name for st in self.states]:
            func(self.get(name), **args)

    def invoke_all(self, func, args):
        for st in self.states:
            self.invoke(func, args, st.name)
