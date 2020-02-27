from typing import TypeVar

import attr

from dfa import DFA


BDD = TypeVar('BDD')


@attr.s(frozen=True, eq=False, auto_attribs=True, repr=False)
class Node:
    horizon: int
    node: BDD
    time: int = 0
    parity: bool = False

    def __eq__(self, other) -> bool:
        return (self.ref, self.time) == (other.ref, other.time)

    @property
    def ref(self) -> int:
        val = self.node.node
        return val if self.parity else -val

    def __str__(self):
        return f"(ref={self.ref}, time={self.time})"

    def __hash__(self):
        return hash((self.ref, self.time))

    @property
    def is_leaf(self):
        return self.node in (self.node.bdd.true, self.node.bdd.false)

    def label(self):
        if not self.is_leaf:
            return None

        return (self.node == self.node.bdd.true) ^ self.parity

    def transition(self, val):
        time = self.time + 1

        if self.is_leaf:
            time = min(self.horizon, time)
            return attr.evolve(self, time=time)

        assert self.time <= self.horizon

        parity = self.parity ^ self.node.negated
        node = self.node.high if val else self.node.low

        return attr.evolve(self, time=time, node=node, parity=parity)


def to_dfa(bdd, lazy=False) -> DFA:
    horizon = len(bdd.manager.vars)

    dfa = DFA(
        start=Node(horizon=horizon, node=bdd, parity=bdd.negated),
        inputs={True, False}, outputs={True, False, None},
        label=Node.label, transition=Node.transition,
    )

    if not lazy:
        dfa.states()  # Traverses and caches all states.

    return dfa
