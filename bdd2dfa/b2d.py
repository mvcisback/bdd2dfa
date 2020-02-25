from dfa import DFA


def to_dfa(bdd, lazy=False) -> DFA:
    true, false = bdd.bdd.true, bdd.bdd.false
    horizon = len(bdd.manager.vars)

    def label(node_t):
        time, node = node_t

        if time < horizon:
            assert node not in (true, false)
            return None

        return node == true

    def transition(node_t, val):
        time, node = node_t
        time += 1

        if node in (true, false):
            time = min(horizon, time)
            return time, node

        assert time <= horizon

        node = node.high if val else node.low
        return time, node

    dfa = DFA(
        start=(0, bdd), inputs={True, False}, outputs={True, False, None},
        label=label, transition=transition,
    )

    if not lazy:
        dfa.states()  # Traverses and caches all states.

    return dfa
