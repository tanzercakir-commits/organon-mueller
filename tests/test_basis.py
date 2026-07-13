import sympy as sp

from organon_mueller.algebra.basis import (
    A,
    A_INV,
    PI,
    Q_I,
    Q_J,
    Q_K,
    Q_ONE,
    SIGMA,
)


def _eq(a: sp.Matrix, b: sp.Matrix) -> bool:
    return all(e == 0 for e in sp.expand(a - b))


def test_a_inverse():
    assert _eq(A * A_INV, sp.eye(4))
    assert _eq(A_INV * A, sp.eye(4))


def test_pauli_algebra():
    for k in (1, 2, 3):
        assert _eq(SIGMA[k] * SIGMA[k], SIGMA[0])
    # anticommutation and cyclic products: s1 s2 = i s3 (etc.)
    assert _eq(SIGMA[1] * SIGMA[2], sp.I * SIGMA[3])
    assert _eq(SIGMA[2] * SIGMA[3], sp.I * SIGMA[1])
    assert _eq(SIGMA[3] * SIGMA[1], sp.I * SIGMA[2])


def test_quaternion_basis_relations():
    """I^2 = J^2 = K^2 = IJK = -1; IJ = K, JK = I, KI = J (Eq. (15))."""
    minus_one = -Q_ONE
    assert _eq(Q_I * Q_I, minus_one)
    assert _eq(Q_J * Q_J, minus_one)
    assert _eq(Q_K * Q_K, minus_one)
    assert _eq(Q_I * Q_J * Q_K, minus_one)
    assert _eq(Q_I * Q_J, Q_K)
    assert _eq(Q_J * Q_K, Q_I)
    assert _eq(Q_K * Q_I, Q_J)
    assert _eq(Q_J * Q_I, -Q_K)


def test_pi_basis_identity_element():
    assert _eq(PI[0][0], sp.eye(4))
