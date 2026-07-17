"""Milestone L0 (FROZEN-7): the Lorentz representation layer.

Everything here is evidence class symbolic-proof (exact expand-based
zero tests) except the final seeded numeric sanity. The two load-bearing
theorems and both anchors were found in the pre-implementation probe and
are locked here permanently.
"""
import numpy as np
import sympy as sp
import pytest

from organon_mueller.lorentz import (
    METRIC,
    SIGMA,
    SIGMA_BAR,
    boost_alpha,
    lorentz_matrix,
    minkowski_square,
    rotation_alpha,
    z_bar_matrix,
    z_inverse,
    z_matrix,
)

A = sp.symbols("a0 a1 a2 a3", complex=True)


def _zero(m: sp.Matrix) -> bool:
    return sp.expand(m) == sp.zeros(*m.shape)


# -- the bridge: Sigma^mu IS the engine's Z-basis ----------------------------------

def test_sigma_is_engine_z_basis():
    """The work order's Σ^μ equals HVector's Z-matrix basis exactly —
    the Mueller↔Lorentz bridge as a theorem (M = ZZ* ↔ Λ = ZZ*)."""
    from organon_mueller import HVector

    for mu in range(4):
        h = [0, 0, 0, 0]
        h[mu] = 1
        assert sp.simplify(HVector(*h).to_z() - SIGMA[mu]) == sp.zeros(4)


# -- structure of the basis --------------------------------------------------------

def test_clifford_relations():
    """Σᵢ² = I and ΣᵢΣⱼ + ΣⱼΣᵢ = 0 for i ≠ j (spatial i, j)."""
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            anti = SIGMA[i] * SIGMA[j] + SIGMA[j] * SIGMA[i]
            expect = 2 * sp.eye(4) if i == j else sp.zeros(4)
            assert _zero(anti - expect), (i, j)


def test_sigma_transpose_equals_conjugate_and_hermitian():
    for s in SIGMA:
        assert s.T == s.conjugate()          # Σ^T = Σ*
        assert s.conjugate().T == s          # Σ† = Σ (hermitian)


# -- theorem 1: Z·Z̄ = (α·α)·I, guard-free, both orders -----------------------------

def test_z_zbar_product_theorem():
    z, zb = z_matrix(A), z_bar_matrix(A)
    q = minkowski_square(A)
    assert _zero(z * zb - q * sp.eye(4))
    assert _zero(zb * z - q * sp.eye(4))


def test_guarded_inverse_corollary():
    """The spec's Z⁻¹ = α_μΣ̄^μ is the α·α = 1 corollary; z_inverse
    divides by the guard quantity and is exact for generic α."""
    z = z_matrix(A)
    zi = z_inverse(A)
    assert sp.simplify(sp.expand(z * zi) - sp.eye(4)) == sp.zeros(4)
    # the degenerate locus is refused with a reason (K26)
    with pytest.raises(ValueError, match="Minkowski square"):
        z_inverse((1, 1, 0, 0))             # (1)^2 - (1)^2 = 0 identically


# -- theorem 2: Λ real, ZZ* = Z*Z, metric factor -----------------------------------

def test_zzstar_commutes_and_lambda_real():
    z = z_matrix(A)
    assert _zero(z * z.conjugate() - z.conjugate() * z)
    lam = lorentz_matrix(A)
    assert _zero(lam - lam.conjugate())      # every entry real


def test_metric_factor_theorem():
    """Λ^T g Λ = (α·α)(α·α)* g for GENERIC complex α; the Lorentz
    property Λ^TgΛ = g is the α·α = 1 corollary."""
    lam = lorentz_matrix(A)
    q = minkowski_square(A)
    lhs = sp.expand(lam.T * METRIC * lam)
    rhs = sp.expand(q * sp.conjugate(q) * METRIC)
    assert _zero(lhs - rhs)


# -- anchors: the known matrices come out exactly ----------------------------------

def test_boost_anchor_textbook_matrix():
    phi = sp.symbols("phi", real=True)
    lam = lorentz_matrix(boost_alpha(phi, (1, 0, 0)))
    expect = sp.Matrix([
        [sp.cosh(phi), sp.sinh(phi), 0, 0],
        [sp.sinh(phi), sp.cosh(phi), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    assert sp.simplify(lam - expect) == sp.zeros(4)


def test_rotation_anchor_block_matrix():
    """z-rotation: R[1][2] = +sin θ, R[2][1] = −sin θ (CONVENTION — the
    spec's own warning: sign differences are conventions, not errors)."""
    th = sp.symbols("theta", real=True)
    lam = lorentz_matrix(rotation_alpha(th, (0, 0, 1)))
    expect = sp.Matrix([
        [1, 0, 0, 0],
        [0, sp.cos(th), sp.sin(th), 0],
        [0, -sp.sin(th), sp.cos(th), 0],
        [0, 0, 0, 1],
    ])
    assert sp.simplify(lam - expect) == sp.zeros(4)


def test_unit_vector_guards():
    with pytest.raises(ValueError, match="unit"):
        boost_alpha(1, (1, 1, 0))
    with pytest.raises(ValueError, match="unit"):
        rotation_alpha(1, (2, 0, 0))
    # a symbolic unit vector is accepted
    a, b = sp.symbols("a b", real=True)
    n = (a / sp.sqrt(a**2 + b**2), b / sp.sqrt(a**2 + b**2), 0)
    assert len(boost_alpha(1, n)) == 4


# -- seeded numeric sanity ---------------------------------------------------------

def test_numeric_sanity_seeded():
    rng = np.random.default_rng(20260716)
    sig = [np.array(s.tolist(), dtype=complex) for s in SIGMA]
    g = np.diag([1.0, -1, -1, -1])
    for _ in range(3):
        a = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        q = a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2
        a = a / np.sqrt(q)                     # guard: alpha.alpha = 1
        z = sum(a[m] * sig[m] for m in range(4))
        lam = z @ z.conj()
        assert np.allclose(lam.imag, 0, atol=1e-10)
        assert np.allclose(lam.T @ g @ lam, g, atol=1e-9)
