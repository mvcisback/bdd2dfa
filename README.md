# bdd2dfa

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/bdd2dfa/status.svg)](https://cloud.drone.io/mvcisback/bdd2dfa)
[![codecov](https://codecov.io/gh/mvcisback/bdd2dfa/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/bdd2dfa)
[![PyPI version](https://badge.fury.io/py/bdd2dfa.svg)](https://badge.fury.io/py/bdd2dfa)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple python wrapper around Binary Decision Diagrams (BDDs) to interpret them
as Deterministic Finite Automata (DFAs).

The package takes as input a BDD from the [`dd` package](https://github.com/tulip-control/dd)
and returns a DFA from the [`dfa` package](https://github.com/mvcisback/dfa).

Formally, the resulting `DFA` objects are quasi-reduced BDDs (QDDs)
where the label of non-leaf states in the original BDD is `None` and
all leaves self loop.


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)

<!-- markdown-toc end -->

# Installation

If you just need to use `bdd2dfa`, you can just run:

`$ pip install bdd2dfa`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

```python
# Create BDD

from dd import BDD

manager.declare('x', 'y', 'z')
x, y, z = map(manager.var, 'xyz')
bexpr = x & y & z


# Convert to DFA

from bdd2dfa import to_dfa

dfa = to_dfa(bexpr)
assert len(dfa.states()) == 7
assert dfa.label([1, 1, 1, 1])
assert not dfa.label([0, 1, 1, 1])
```
