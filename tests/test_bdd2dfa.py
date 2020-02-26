from itertools import product

from dd import BDD

from bdd2dfa import to_dfa


def test_and():
    manager = BDD()
    manager.declare('x', 'y', 'z')

    x, y, z = map(manager.var, 'xyz')
    bexpr = x & y & z

    dfa = to_dfa(bexpr)

    assert len(dfa.states()) == 7
    assert dfa.label([1, 1, 1, 1])
    assert not dfa.label([0, 1, 1, 1])
    assert dfa.label([1, 1]) is None

    s1 = dfa.transition([])
    s2 = dfa.transition([0])
    s3 = dfa.transition([0, 0])

    assert s1 != s2 != s3
    assert s3 == dfa.transition([1, 0])


def xor(x, y):
    return (x | y) & ~(x & y)


def test_parity():
    manager = BDD()
    manager.declare('x', 'y', 'z')

    x, y, z = map(manager.var, 'xyz')

    bexpr = xor(xor(x, y), z)

    dfa = to_dfa(bexpr)

    assert len(dfa.states()) == 7

    for word in product([0, 1], [0, 1], [0, 1]):
        assert dfa.label(word) == (sum(word) % 2)
