from __future__ import annotations

from itertools import product
from typing import TypeVar

import attr

from dfa import DFA


BDD = TypeVar('BDD')


@attr.s(frozen=True, auto_detect=True, auto_attribs=True)
class BNode:
    node: BDD
    parity: bool = False

    def __eq__(self, other) -> bool:
        return self.ref == other.ref

    @property
    def ref(self) -> int:
        node = self.node if self.parity else ~self.node
        return int(node)

    def __repr__(self):
        return str(self.ref)

    def __hash__(self):
        return self.ref

    @property
    def is_leaf(self):
        return self.node in (self.node.bdd.true, self.node.bdd.false)

    def label(self):
        if not self.is_leaf:
            return self.node.var

        return (self.node == self.node.bdd.true) ^ self.parity

    def transition(self, val):
        if self.is_leaf:
            return self

        parity = self.parity ^ self.node.negated
        node = self.node.high if val else self.node.low
        return attr.evolve(self, node=node, parity=parity)

    @property
    def level(self):
        if self.is_leaf:
            return len(self.node.bdd.vars)
        return self.node.level

    def as_qnode(self) -> QNode:
        return QNode(self.node, self.parity, self.level)


@attr.s(frozen=True, auto_attribs=True, auto_detect=True)
class QNode(BNode):
    debt: int = 0

    def __eq__(self, other):
        return (self.ref == other.ref) and (self.debt == other.debt)

    def __hash__(self):
        return hash((self.ref, self.debt))

    def __repr__(self):
        return f"(ref={self.ref}, debt={self.debt})"

    def transition(self, val):
        if self.debt == 0:
            state2 = super().transition(val)
            debt = max(state2.level - self.level - 1, 0)
            return QNode(state2.node, state2.parity, debt)

        debt = max(0, self.debt - 1)
        return attr.evolve(self, debt=debt)

    def label(self):
        return (self.debt, super().label())


def to_dfa(bdd, lazy=False, qdd=True) -> DFA:
    start = BNode(node=bdd)
    if qdd:
        start = start.as_qnode()
    Node = type(start)

    levels = range(len(bdd.bdd.vars))
    bdd_labels = set(bdd.bdd.vars) | {True, False}

    dfa = DFA(
        start=start,
        inputs={True, False},
        outputs=product(levels, bdd_labels),
        label=Node.label, transition=Node.transition,
    )

    if not lazy:
        dfa.states()  # Traverses and caches all states.

    return dfa
