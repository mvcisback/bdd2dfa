from typing import TypeVar

import attr

from dfa import DFA


BDD = TypeVar('BDD')


@attr.s(frozen=True, eq=False, auto_attribs=True, repr=False)
class BNode:
    node: BDD
    parity: bool = False

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    @property
    def ref(self) -> int:
        val = self.node.node
        return -val if self.parity else val

    def __str__(self):
        return str(self.ref)

    def __hash__(self):
        return hash(str(self))

    @property
    def is_leaf(self):
        return self.node in (self.node.bdd.true, self.node.bdd.false)

    def label(self):
        if not self.is_leaf:
            return None

        return (self.node == self.node.bdd.true) ^ self.parity

    def transition(self, val):
        if self.is_leaf:
            return self

        parity = self.parity ^ self.node.negated
        node = self.node.high if val else self.node.low
        return attr.evolve(self, node=node, parity=parity)


@attr.s(frozen=True, eq=False, auto_attribs=True, repr=False)
class QNode(BNode):
    debt: int = 0

    def __str__(self):
        return f"(ref={self.ref}, debt={self.debt})"

    def transition(self, val):
        debt = max(0, self.debt - 1)

        if debt == 0:
            state2 = super().transition(val)
            debt = max(state2.node.level - self.node.level - 1, 0)
            return QNode(state2.node, state2.parity, debt)

        return attr.evolve(self, debt=debt)

    def label(self):
        return None if self.debt > 0 else super().label()


def to_dfa(bdd, lazy=False, qdd=True) -> DFA:
    Node = QNode if qdd else BNode
    start = Node(node=bdd)

    dfa = DFA(
        start=start, inputs={True, False}, outputs={True, False, None},
        label=Node.label, transition=Node.transition,
    )

    if not lazy:
        dfa.states()  # Traverses and caches all states.

    return dfa
