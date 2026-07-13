"""Stage-8: the symmetry-conditioned decomposition deriver (AO2016).

Acceptance (spec stage-08):
  A  derived equations == paper Table 2, symbolically, all six variants
  B  the paper's Section-6 numeric example reproduces to print precision
  C  synthetic roundtrips recover components and weights (exact data)
  D  degenerate (same-symmetry) mixtures raise, never mis-decompose
  +  basis-distinction sentinel (standard vs Pi covariance are different)
"""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.algebra.states import covariance_from_mueller
from organon_mueller.decomposition import (
    DecompositionError,
    decompose,
    derive_equations,
    mueller_from_standard_covariance,
    standard_covariance_from_mueller,
)
from organon_mueller.decomposition.covariance import SYMMETRY_TEMPLATES
from organon_mueller.decomposition.derive import generic_hermitian

RNG_SEED = 20260713


# -- A: derived == Table 2 (rule K28: exact symbolic zero) --------------------

_H = generic_hermitian()
_h = lambda i, j: _H[i, j]  # noqa: E731

# NOTE on the 2b/3b anchors: the paper's print renders the first-solved
# parameter as "alpha1K"/"alpha1E", but it is the CENTER parameter
# (alpha1*Kbar / alpha1*Ebar) — the OCR demonstrably strips overbars
# (Table 1's "Pbar = 1 - P" prints as "P = 1 - P"), the central minor
# structurally determines the center parameter, and the paper's own
# Eq. (20) labels the 3b value 0.0067 as alpha1*Ebar. The 3a w-anchor is
# the elementwise conjugate of the paper's V*-equation. (Stage-8 review
# re-derived all six variants independently and confirmed exact matches.)
TABLE2_ANCHORS = {
    ("type1", "a"): (
        (_h(1, 1) * _h(0, 0) - _h(1, 0) * _h(0, 1)) / _h(1, 1),
        lambda x: (_h(1, 0) * _h(0, 3) - _h(1, 3) * (_h(0, 0) - x)) / _h(1, 0),
    ),
    ("type1", "b"): (
        (_h(2, 2) * _h(0, 0) - _h(2, 0) * _h(0, 2)) / _h(2, 2),
        lambda x: (_h(2, 0) * _h(0, 3) - _h(2, 3) * (_h(0, 0) - x)) / _h(2, 0),
    ),
    ("type2", "a"): (
        (_h(3, 0) * _h(0, 3) - _h(0, 0) * _h(3, 3))
        / (_h(3, 0) + _h(0, 3) - _h(3, 3) - _h(0, 0)),
        lambda x: (_h(3, 0) * _h(0, 1) - _h(0, 0) * _h(3, 1) + x * (_h(3, 1) - _h(0, 1)))
        / (_h(3, 0) - _h(0, 0)),
    ),
    ("type2", "b"): (
        (_h(2, 1) * _h(1, 2) - _h(1, 1) * _h(2, 2))
        / (_h(2, 1) + _h(1, 2) - _h(2, 2) - _h(1, 1)),
        lambda x: (_h(1, 1) * _h(0, 2) - _h(1, 2) * _h(0, 1) + x * (_h(0, 1) - _h(0, 2)))
        / (_h(1, 1) - _h(1, 2)),
    ),
    # paper's 3a solves alpha1*V^* on the conjugate side; anchored here as
    # its elementwise conjugate (h real diagonal, conj(h10)=h01, ...)
    ("type3", "a"): (
        (_h(3, 0) * _h(0, 3) - _h(0, 0) * _h(3, 3))
        / (_h(3, 0) + _h(0, 3) - _h(3, 3) - _h(0, 0)),
        lambda x: (_h(0, 1) * _h(3, 0) - _h(0, 0) * _h(3, 1) + x * (_h(3, 1) - _h(0, 1)))
        / (_h(3, 0) - _h(0, 0)),
    ),
    ("type3", "b"): (
        (_h(1, 1) * _h(2, 2) - _h(2, 1) * _h(1, 2))
        / (_h(2, 1) + _h(1, 2) + _h(2, 2) + _h(1, 1)),
        lambda x: (_h(0, 1) * _h(1, 2) - _h(1, 1) * _h(0, 2) + x * (_h(0, 1) + _h(0, 2)))
        / (_h(1, 1) + _h(1, 2)),
    ),
}


@pytest.mark.parametrize("key", sorted(TABLE2_ANCHORS), ids=lambda k: f"{k[0]}{k[1]}")
def test_a_derived_equations_match_paper_table2(key):
    symmetry, variant = key
    anchor_x, anchor_w = TABLE2_ANCHORS[key]
    eq = derive_equations(symmetry, variant)
    assert sp.simplify(eq.x_expr - anchor_x) == 0
    assert sp.simplify(eq.w_expr - anchor_w(anchor_x)) == 0


# -- B: paper Section-6 numeric anchor -----------------------------------------

M1_PAPER = np.array(
    [[1, 0, 0, 0.1489], [0, 0.9108, 0.3851, 0],
     [0, -0.3851, 0.9108, 0], [0.1489, 0, 0, 1]]
)
M2_PAPER = np.array(
    [[1, 0.0544, 0.6124, 0.2719], [0.2502, 0.7064, 0.2447, 0.2273],
     [0.6124, -0.2146, 0.8118, 0.4669], [-0.1196, -0.0768, -0.4519, 0.5935]]
)


@pytest.mark.parametrize("variant", ["a", "b"])
def test_b_paper_numeric_example(variant):
    mix = 0.3 * M1_PAPER + 0.7 * M2_PAPER
    r = decompose(
        mueller=mix, symmetry="type3", variant=variant,
        rank_tol=1e-4, psd_tol=1e-3, rank1_tol=1e-2,  # 4-decimal print noise
    )
    assert abs(r.alpha1 - 0.3) < 1e-3
    assert abs(r.h1_scaled[0, 0].real - 0.1433) < 3e-4      # alpha1*E
    assert abs(r.h1_scaled[0, 1] - (0.0289 + 0.0112j)) < 3e-4  # alpha1*V
    assert abs(r.h1_scaled[1, 1].real - 0.0067) < 3e-4      # alpha1*Ebar
    assert abs(r.h1[0, 0].real - 0.4777) < 3e-4             # H1 (Eq. 21)
    assert abs(r.h1[0, 1] - (0.0962 + 0.0372j)) < 3e-4
    assert np.max(np.abs(r.m1 - M1_PAPER)) < 1e-3
    assert np.max(np.abs(r.m2 - M2_PAPER)) < 1e-3


# -- C: synthetic exact roundtrips ----------------------------------------------

def _random_symmetric_pure(symmetry: str, rng) -> np.ndarray:
    """Random normalized pure H of the given type (Table 1 constraints)."""
    template, _ = SYMMETRY_TEMPLATES[symmetry]
    x = float(rng.uniform(0.15, 0.35 if symmetry != "type1" else 0.85))
    total = 1.0 if symmetry == "type1" else 0.5
    xbar = total - x
    mag = np.sqrt(x * xbar)
    phase = float(rng.uniform(0, 2 * np.pi))
    w = mag * np.exp(1j * phase)
    xs, ws = sp.symbols("xs", positive=True), sp.symbols("ws", complex=True)
    h = template(xs, ws).subs({xs: x, ws: sp.sympify(w)})
    return np.array(sp.matrix2numpy(sp.Matrix(h).evalf(), dtype=complex))


def _random_generic_pure(rng) -> np.ndarray:
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u = u / np.linalg.norm(u)
    return np.outer(u, u.conj())


@pytest.mark.parametrize("symmetry", ["type1", "type2", "type3"])
@pytest.mark.parametrize("variant", ["a", "b"])
def test_c_synthetic_roundtrip(symmetry, variant):
    rng = np.random.default_rng(RNG_SEED)
    for _ in range(3):
        h1 = _random_symmetric_pure(symmetry, rng)
        h2 = _random_generic_pure(rng)
        alpha1 = float(rng.uniform(0.25, 0.75))
        cov = alpha1 * h1 + (1 - alpha1) * h2
        r = decompose(covariance=cov, symmetry=symmetry, variant=variant)
        assert abs(r.alpha1 - alpha1) < 1e-8
        assert np.max(np.abs(r.h1 - h1)) < 1e-7
        assert np.max(np.abs(r.h2 - h2)) < 1e-7


def test_c_mueller_covariance_roundtrip():
    rng = np.random.default_rng(RNG_SEED)
    h = 0.4 * _random_generic_pure(rng) + 0.6 * _random_generic_pure(rng)
    m = mueller_from_standard_covariance(sp.Matrix(h))
    back = standard_covariance_from_mueller(m)
    diff = np.array(sp.matrix2numpy((back - sp.Matrix(h)).evalf(), dtype=complex))
    assert np.max(np.abs(diff)) < 1e-12


# -- D: degenerate same-symmetry mixture must raise ------------------------------

def test_d_same_symmetry_overlap_raises():
    rng = np.random.default_rng(RNG_SEED)
    h1 = _random_symmetric_pure("type1", rng)
    h2 = _random_symmetric_pure("type1", rng)
    cov = 0.4 * h1 + 0.6 * h2
    with pytest.raises(DecompositionError):
        decompose(covariance=cov, symmetry="type1", variant="auto")


def test_d_rank_guard():
    rng = np.random.default_rng(RNG_SEED)
    cov = _random_generic_pure(rng)  # rank 1
    with pytest.raises(DecompositionError):
        decompose(covariance=cov, symmetry="type1")


# -- basis-distinction sentinel (decision M29) -----------------------------------

def test_standard_and_pi_covariances_differ():
    m = sp.Matrix(M1_PAPER)
    std = standard_covariance_from_mueller(m)
    pi = covariance_from_mueller(m)
    diff = np.array(sp.matrix2numpy((std - pi).evalf(), dtype=complex))
    assert np.max(np.abs(diff)) > 0.05  # different objects, never mix
