"""Fixed algebraic bases for the Stokes-Mueller formalism.

Conventions are pinned to the Kuntman-Arteaga papers (architectural
decision M5 of stage-00):

* Pauli order: sigma0 = identity, sigma1 = diag(1, -1),
  sigma2 = off-diagonal ones, sigma3 = [[0, -i], [i, 0]].
  (JOSA A 34, 80 (2017), Eqs. (2)-(3).)
* A matrix and its inverse: JOSA A 34, 80 (2017), Eq. (5).
* Quaternion basis matrices ONE, I, J, K: arXiv:1705.07147, Eq. (14).
"""
from __future__ import annotations

import sympy as sp

__all__ = [
    "SIGMA",
    "A",
    "A_INV",
    "PI",
    "Q_ONE",
    "Q_I",
    "Q_J",
    "Q_K",
]

_i = sp.I

#: Pauli matrices (with the 2x2 identity first).
SIGMA = (
    sp.Matrix([[1, 0], [0, 1]]),
    sp.Matrix([[1, 0], [0, -1]]),
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[0, -_i], [_i, 0]]),
)

#: Basis-change matrix A (JOSA A 34, 80, Eq. (5)).
A = sp.Matrix(
    [
        [1, 0, 0, 1],
        [1, 0, 0, -1],
        [0, 1, 1, 0],
        [0, _i, -_i, 0],
    ]
)

#: A^{-1} = (1/2) A^dagger.
A_INV = sp.Rational(1, 2) * A.H


def _pi(i: int, j: int) -> sp.Matrix:
    """Transformed basis element Pi_ij = A (sigma_i kron sigma_j^*) A^{-1}."""
    kron = sp.Matrix(sp.kronecker_product(SIGMA[i], SIGMA[j].conjugate()))
    return sp.simplify(A * kron * A_INV)


#: Pi basis, PI[i][j] = A (sigma_i kron sigma_j^*) A^{-1}  (JOSA A 34, 80, Eq. (4)).
PI = tuple(tuple(_pi(i, j) for j in range(4)) for i in range(4))

#: 4x4 matrix representation of the quaternion basis (arXiv:1705.07147, Eq. (14)).
Q_ONE = sp.eye(4)

Q_I = sp.Matrix(
    [
        [0, -_i, 0, 0],
        [-_i, 0, 0, 0],
        [0, 0, 0, -1],
        [0, 0, 1, 0],
    ]
)

Q_J = sp.Matrix(
    [
        [0, 0, -_i, 0],
        [0, 0, 0, 1],
        [-_i, 0, 0, 0],
        [0, -1, 0, 0],
    ]
)

Q_K = sp.Matrix(
    [
        [0, 0, 0, -_i],
        [0, 0, -1, 0],
        [0, 1, 0, 0],
        [-_i, 0, 0, 0],
    ]
)
