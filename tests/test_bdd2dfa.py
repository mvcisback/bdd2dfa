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
    assert dfa.label([1, 1, 1, 1]) == (0, True)
    assert dfa.label([0, 1, 1, 1]) == (0, False)
    assert dfa.label([1, 1]) == (0, 'z')

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
        debt, label = dfa.label(word)
        assert debt == 0
        assert label == (sum(word) % 2)


def test_negated_parity():
    manager = BDD()
    manager.declare('x', 'y', 'z')

    x, y, z = map(manager.var, 'xyz')

    bexpr = ~xor(xor(x, y), z)

    dfa = to_dfa(bexpr)

    assert len(dfa.states()) == 7

    for word in product([0, 1], [0, 1], [0, 1]):
        debt, label = dfa.label(word)
        assert debt == 0
        assert label != (sum(word) % 2)


def test_bnode():
    manager = BDD()
    manager.declare('x', 'y', 'z')

    x, y, z = map(manager.var, 'xyz')

    bexpr = x & y & z
    dfa = to_dfa(bexpr, qdd=False)
    assert len(dfa.states()) == 5


def test_draw():
    from tempfile import NamedTemporaryFile
    from dfa.draw import write_dot

    manager = BDD()
    manager.declare('x', 'y', 'z')

    x, y, z = map(manager.var, 'xyz')
    bexpr = x & y & z
    dfa = to_dfa(bexpr)

    with NamedTemporaryFile() as f:
        write_dot(dfa, f.name)


def test_true():
    manager = BDD()
    manager.declare('x', 'y', 'z')

    bexpr = manager.true

    dfa = to_dfa(bexpr)

    assert len(dfa.states()) == 4
    assert dfa.label([1, 1, 1, 1]) == (0, True)
    assert dfa.label([0, 1, 1, 1]) == (0, True)
    assert dfa.label([1, 1]) == (1, True)

    dfa = to_dfa(bexpr, qdd=False)
    assert len(dfa.states()) == 1


def test_skip():
    manager = BDD()
    manager.declare('x', 'y', 'z')
    manager.declare('x', 'y', 'z')

    bexpr = manager.var(manager.var_at_level(2))
    dfa = to_dfa(bexpr)

    assert len(dfa.states()) == 5
    assert dfa.label([1, 1, 1]) == (0, True)
    assert dfa.label([0, 1, 1]) == (0, True)
    assert dfa.label([0, 1, 0]) == (0, False)
    assert dfa.label([1, 1]) == (0, 'z')

    dfa = to_dfa(bexpr, qdd=False)
    assert len(dfa.states()) == 3

    bexpr &= manager.var(manager.var_at_level(0))
    dfa = to_dfa(bexpr)

    assert len(dfa.states()) == 7
    assert dfa.label([1, 0, 1]) == (0, True)
    assert dfa.label([1, 1, 1]) == (0, True)
    assert dfa.label([0, 1, 1]) == (0, False)
    assert dfa.label([0, 1, 0]) == (0, False)
    assert dfa.label([1, 1, 0]) == (0, False)
    assert dfa.label([1, 1]) == (0, 'z')
