#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from transcripts18xx.engine.states import state


class TestState(unittest.TestCase):

    def setUp(self) -> None:
        self.state = state.State('state1')

    def test_repr(self):
        self.assertEqual(
            "State(name='state1', cash=0, privates={})", self.state.__repr__()
        )

    def test_collects(self):
        self.state.collects(40)
        self.assertEqual(40, self.state.cash)

    def test_buys_private(self):
        self.state.buys_private('private1', 100, 200)
        self.assertEqual(dict(private1=200), self.state.privates)
        self.assertEqual(-100, self.state.cash)

    def test_private_closes(self):
        self.state.privates['private1'] = 100
        self.state.private_closes('private1')
        self.assertEqual(dict(), self.state.privates)

    def test_private_closes_non_existing(self):
        self.state.privates['private1'] = 100
        self.state.private_closes('private2')
        self.assertEqual(dict(private1=100), self.state.privates)

    def test_private_closes_all(self):
        self.state.privates['private1'] = 100
        self.state.privates['private2'] = 80
        self.state.private_closes()
        self.assertEqual(dict(), self.state.privates)


class TestStates(unittest.TestCase):

    def setUp(self) -> None:
        self.states = state.States()
        self.states.states = [
            state.State(name) for name in ['state1', 'state2', 'state3']
        ]

    def test_repr(self):
        self.assertEqual(
            str(
                "State(name='state1', cash=0, privates={})\n"
                "State(name='state2', cash=0, privates={})\n"
                "State(name='state3', cash=0, privates={})\n"
            ),
            self.states.__repr__()
        )

    def test_get(self):
        self.assertEqual('state1', self.states.get('state1').name)
        self.assertEqual('state3', self.states.get('state3').name)

    def test_invoke(self):
        self.states.invoke(
            state.State.collects, dict(amount=10), name='state1'
        )
        self.assertEqual([10, 0, 0], [st.cash for st in self.states.states])

    def test_invoke_all(self):
        self.states.invoke_all(state.State.collects, dict(amount=20))
        self.assertEqual([20, 20, 20], [st.cash for st in self.states.states])
