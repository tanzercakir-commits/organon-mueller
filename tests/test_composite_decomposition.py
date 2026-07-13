"""Stage-9(a): composite symmetries (AO2016 Tables 3-4) — deriver + solver."""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.decomposition.composite import (
    TYPE12,
    TYPE13,
    TYPE23,
    decompose_composite,
    derive_composite,
)
from organon_mueller.decomposition.derive import generic_hermitian
from organon_mueller.decomposition.solve import DecompositionError

_H = generic_hermitian()
_h = lambda i, j: _H[i, j]  # noqa: E731

# Table 4, entered by hand as anchors only (M28); same overbar/conjugate
# reading conventions as stage 8 (see tests/test_decomposition.py note).
TABLE4_ANCHORS = {
    TYPE12: (
        (_h(2, 1) * _h(1, 2) - _h(1, 1) * _h(2, 2))
        / (_h(2, 1) + _h(1, 2) - _h(2, 2) - _h(1, 1)),
        lambda x: (_h(0, 2) * _h(1, 1) - _h(0, 1) * _h(1, 2) + x * (_h(0, 1) - _h(0, 2)))
        / (_h(1, 1) - _h(1, 2)),
        lambda x: (_h(3, 1) * _h(2, 2) - _h(2, 1) * _h(3, 2) - x * (_h(3, 1) - _h(3, 2)))
        / (_h(2, 2) - _h(2, 1)),
    ),
    TYPE13: (
        (_h(1, 1) * _h(2, 2) - _h(2, 1) * _h(1, 2))
        / (_h(1, 1) + _h(2, 2) + _h(2, 1) + _h(1, 2)),
        lambda x: (_h(0, 1) * _h(1, 2) - _h(1, 1) * _h(0, 2) + x * (_h(0, 1) + _h(0, 2)))
        / (_h(1, 1) + _h(1, 2)),
        lambda x: (_h(3, 1) * _h(2, 2) - _h(2, 1) * _h(3, 2) - x * (_h(3, 1) + _h(3, 2)))
        / (_h(2, 2) + _h(2, 1)),
    ),
    TYPE23: (
        (_h(3, 0) * _h(0, 3) - _h(0, 0) * _h(3, 3))
        / (_h(3, 0) + _h(0, 3) - _h(3, 3) - _h(0, 0)),
        lambda x: (_h(1, 0) * _h(0, 3) - _h(0, 0) * _h(1, 3) - x * (_h(1, 0) - _h(1, 3)))
        / (_h(0, 3) - _h(0, 0)),
        lambda x: (_h(2, 0) * _h(0, 3) - _h(0, 0) * _h(2, 3) - x * (_h(2, 0) - _h(2, 3)))
        / (_h(0, 3) - _h(0, 0)),
    ),
}


@pytest.mark.parametrize("symmetry", [TYPE12, TYPE13, TYPE23])
def test_derived_equations_match_table4(symmetry):
    ax, ag, ah = TABLE4_ANCHORS[symmetry]
    d = derive_composite(symmetry)
    assert sp.simplify(d.x_expr - ax) == 0
    assert sp.simplify(d.g_expr - ag(ax)) == 0
    assert sp.simplify(d.h_expr - ah(ax)) == 0


def _pure_from_u(u) -> np.ndarray:
    u = np.array(u, dtype=complex)
    u = u / np.linalg.norm(u)
    return np.outer(u, u.conj())


def _symmetric_u(symmetry, rng):
    c = lambda: complex(rng.standard_normal(), rng.standard_normal())  # noqa: E731
    if symmetry == TYPE12:
        u1 = c()
        return [c(), u1, u1, c()]
    if symmetry == TYPE13:
        u1 = c()
        return [c(), u1, -u1, c()]
    u0 = c()
    return [u0, c(), c(), u0]


@pytest.mark.parametrize("symmetry", [TYPE12, TYPE13, TYPE23])
def test_synthetic_roundtrip(symmetry):
    rng = np.random.default_rng(20260713)
    for _ in range(3):
        h1 = _pure_from_u(_symmetric_u(symmetry, rng))
        h2 = _pure_from_u([complex(rng.standard_normal(), rng.standard_normal())
                           for _ in range(4)])
        alpha1 = float(rng.uniform(0.25, 0.75))
        cov = alpha1 * h1 + (1 - alpha1) * h2
        r = decompose_composite(cov, symmetry)
        assert abs(r.alpha1 - alpha1) < 1e-8
        assert np.max(np.abs(r.h1 - h1)) < 1e-7
        assert np.max(np.abs(r.h2 - h2)) < 1e-7


@pytest.mark.parametrize("symmetry", [TYPE12, TYPE13, TYPE23])
def test_missing_anisotropy_guard(symmetry):
    """Paper requirement: the other component must carry the missing
    anisotropy type; a same-symmetry second component collapses the
    guard denominator and must raise (all three types — review sug. 3)."""
    rng = np.random.default_rng(20260713)
    h1 = _pure_from_u(_symmetric_u(symmetry, rng))
    h2 = _pure_from_u(_symmetric_u(symmetry, rng))  # same symmetry: overlap
    cov = 0.4 * h1 + 0.6 * h2
    with pytest.raises(DecompositionError):
        decompose_composite(cov, symmetry)


def test_rank_guard():
    rng = np.random.default_rng(20260713)
    cov = _pure_from_u([complex(rng.standard_normal(), rng.standard_normal())
                        for _ in range(4)])
    with pytest.raises(DecompositionError):
        decompose_composite(cov, TYPE12)
