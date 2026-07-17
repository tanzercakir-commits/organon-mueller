"""Milestone L1 (FROZEN-7): the work order's five Task-1 identities.

Everything here is evidence class symbolic-proof. The five identities
are locked in their strongest form — guard-free theorems over generic
complex α — and the spec's literal forms are locked as q = 1 corollaries
for both boosts and rotations. The one convention the mathematics forces
(row-index Λ^μ_ν) is pinned by a NEGATIVE test.
"""
import sympy as sp
import pytest

from organon_mueller.lorentz import (
    LORENTZ_TASK1,
    SIGMA,
    boost_alpha,
    rotation_alpha,
    spec_form_holds,
    verify_task1,
    z_bar_matrix,
    z_matrix,
)

A = sp.symbols("b0 b1 b2 b3", complex=True)


def _zero(m):
    return sp.expand(m) == sp.zeros(4)


# -- the five guard-free theorems --------------------------------------------------

def test_registry_complete_and_all_proven():
    assert [e.key for e in LORENTZ_TASK1] == ["LT1", "LT2", "LT3",
                                              "LT4", "LT5"]
    assert verify_task1() == {f"LT{k}": True for k in range(1, 6)}


def test_lt1_direct_and_row_convention():
    """Independent re-statement (not via the registry): Z†Σ^μZ equals the
    ROW combination Λ^μ_νΣ^ν for generic complex α."""
    z = z_matrix(A)
    zd, lam = z.conjugate().T, sp.expand(z * z.conjugate())
    for m in range(4):
        row = sum((lam[m, n] * SIGMA[n] for n in range(4)), sp.zeros(4))
        assert _zero(zd * SIGMA[m] * z - row)


def test_lt1_column_convention_is_false():
    """NEGATIVE pin: with the column combination Λ^ν_μ the identity is
    NOT an identity — the index convention is forced, not chosen."""
    z = z_matrix(A)
    zd, lam = z.conjugate().T, sp.expand(z * z.conjugate())
    col_ok = all(
        _zero(zd * SIGMA[m] * z
              - sum((lam[n, m] * SIGMA[n] for n in range(4)),
                    sp.zeros(4)))
        for m in range(4))
    assert not col_ok


def test_lt2_to_lt5_direct():
    """Independent re-statement of the four sandwich theorems with their
    exact scalar factors (q for transpose, q̄ for conjugate)."""
    z, zb = z_matrix(A), z_bar_matrix(A)
    q = sp.expand(A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2)
    qc = sp.conjugate(q)
    for m in range(4):
        assert _zero(z.conjugate() * SIGMA[m] * zb.conjugate()
                     - qc * SIGMA[m])
        assert _zero(zb.conjugate() * SIGMA[m] * z.conjugate()
                     - qc * SIGMA[m])
        assert _zero(z.T * SIGMA[m] * zb.T - q * SIGMA[m])
        assert _zero(zb.T * SIGMA[m] * z.T - q * SIGMA[m])


def test_chain_lemma_lambda_z_times_lambda_zbar():
    """Λ(Z)·Λ(Z̄) = q q̄ I — the lemma that turns LT1 into the spec's
    I1 on the guard."""
    z, zb = z_matrix(A), z_bar_matrix(A)
    q = A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2
    prod = sp.expand((z * z.conjugate()) * (zb * zb.conjugate()))
    assert _zero(prod - q * sp.conjugate(q) * sp.eye(4))


# -- the spec's literal forms on the guard (boosts AND rotations) ------------------

@pytest.mark.parametrize("which", ["I1", "I2", "I3", "I4", "I5"])
def test_spec_forms_hold_for_boost_and_rotation(which):
    phi = sp.symbols("phi", real=True)
    th = sp.symbols("theta", real=True)
    assert spec_form_holds(boost_alpha(phi, (1, 0, 0)), which)
    assert spec_form_holds(rotation_alpha(th, (0, 0, 1)), which)


def test_spec_form_guard_is_enforced():
    with pytest.raises(ValueError, match="guard"):
        spec_form_holds((2, 0, 0, 0), "I2")     # q = 4 != 1
    with pytest.raises(ValueError, match="which"):
        spec_form_holds((1, 0, 0, 0), "I9")


# -- the conjugation lemma behind the spec's sign warning --------------------------

def test_conjugation_lemma_general_and_parametrized():
    """General lemma (guard-free): Z(α)* = Z(α*)ᵀ — because Σ* = Σᵀ.
    At the PARAMETER level conjugation reverses rotations and fixes
    boosts: rotation_alpha(θ)* = rotation_alpha(−θ) componentwise, and
    boost_alpha is real. (An earlier, WRONG chat-level phrasing —
    Z(rot θ)* = Z(rot −θ) without the transpose — was caught by this
    test's first version; the honest record lives here.)"""
    z = z_matrix(A)
    z_conj_params = z_matrix(tuple(sp.conjugate(a) for a in A))
    assert sp.expand(z.conjugate() - z_conj_params.T) == sp.zeros(4)

    th = sp.symbols("theta", real=True)
    rot = rotation_alpha(th, (0, 0, 1))
    rot_neg = rotation_alpha(-th, (0, 0, 1))
    assert all(sp.simplify(sp.conjugate(rot[m]) - rot_neg[m]) == 0
               for m in range(4))
    phi = sp.symbols("phi", real=True)
    b = boost_alpha(phi, (1, 0, 0))
    assert all(sp.simplify(sp.conjugate(b[m]) - b[m]) == 0
               for m in range(4))
    # matrix-level corollaries, with the transpose where it belongs
    zr = z_matrix(rot)
    assert sp.expand(zr.conjugate() - z_matrix(rot_neg).T) == sp.zeros(4)
    zb_ = z_matrix(b)
    assert sp.expand(zb_.conjugate() - zb_.T) == sp.zeros(4)
