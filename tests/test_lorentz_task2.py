"""Milestone L2 (FROZEN-7): the five Σ̄ identities the work order's
Task 2 asks for — found, then locked.

Everything here is evidence class symbolic-proof. The discovery route
(probes/probe-lorentz-task2.py) used trace-orthogonality of the Σ basis
to EXTRACT the coefficient matrix of the Λ-type identity, then
identified it: C = gΛᵀg = Λ(Z̄) — the equality of the two
identifications is itself a bonus theorem, Λ(Z̄) = gΛ(Z)ᵀg, guard-free.
On the guard q = 1 this makes C = Λ⁻¹, so the spec-mirror form
Σ̄^μ = Λ^μ_ν Z Σ̄^ν Z† is the exact dual of Task-1's I1. Wrong
candidates for C (plain Λ, Λᵀ, gΛg) are pinned FALSE by negative tests.
"""
import sympy as sp
import pytest

from organon_mueller.lorentz import (
    LORENTZ_TASK2,
    METRIC,
    SIGMA,
    SIGMA_BAR,
    bonus_lambda_zbar_theorem,
    boost_alpha,
    rotation_alpha,
    spec_form_holds_bar,
    verify_task2,
    z_bar_matrix,
    z_matrix,
)

A = sp.symbols("c0 c1 c2 c3", complex=True)


def _zero(m):
    return sp.expand(m) == sp.zeros(4)


def _exp_zero(m):
    """Zero test for half-angle trig/hyperbolic content (L1 lesson)."""
    return sp.simplify(sp.expand(m.rewrite(sp.exp))) == sp.zeros(4)


# -- the extraction lemma the discovery probe relied on ----------------------------

def test_trace_orthogonality_of_both_bases():
    """tr(Σ^μ Σ^ν) = 4δ^{μν} (and likewise for Σ̄): the lemma that lets
    coefficient matrices be EXTRACTED exactly by traces."""
    for i in range(4):
        for j in range(4):
            want = 4 if i == j else 0
            assert sp.trace(SIGMA[i] * SIGMA[j]) == want
            assert sp.trace(SIGMA_BAR[i] * SIGMA_BAR[j]) == want


# -- the five Σ̄ theorems ----------------------------------------------------------

def test_registry_complete_and_all_proven():
    assert [e.key for e in LORENTZ_TASK2] == ["LT6", "LT7", "LT8",
                                              "LT9", "LT10"]
    assert verify_task2() == {f"LT{k}": True for k in range(6, 11)}


def test_lt6_direct_with_both_identifications():
    """Independent re-statement (not via the registry): Z Σ̄^μ Z† equals
    the ROW combination C^μ_ν Σ̄^ν for generic complex α, with C given by
    BOTH closed forms — C = gΛᵀg and C = Λ(Z̄)."""
    z, zb = z_matrix(A), z_bar_matrix(A)
    zd, lam = z.conjugate().T, sp.expand(z * z.conjugate())
    for c in (sp.expand(METRIC * lam.T * METRIC),
              sp.expand(zb * zb.conjugate())):
        for m in range(4):
            row = sum((c[m, n] * SIGMA_BAR[n] for n in range(4)),
                      sp.zeros(4))
            assert _zero(z * SIGMA_BAR[m] * zd - row)


def test_lt6_wrong_coefficient_matrices_are_pinned_false():
    """NEGATIVE pins: C is NOT plain Λ, NOT Λᵀ, NOT gΛg — the closed
    form gΛᵀg is forced, not chosen."""
    z = z_matrix(A)
    zd, lam = z.conjugate().T, sp.expand(z * z.conjugate())
    for wrong in (lam, lam.T, sp.expand(METRIC * lam * METRIC)):
        ok = all(
            _zero(z * SIGMA_BAR[m] * zd
                  - sum((wrong[m, n] * SIGMA_BAR[n] for n in range(4)),
                        sp.zeros(4)))
            for m in range(4))
        assert not ok


def test_bonus_theorem_lambda_zbar_is_g_lambdaT_g():
    """BONUS theorem, guard-free: Λ(Z̄) = g Λ(Z)ᵀ g — independent
    re-statement plus the registry function."""
    z, zb = z_matrix(A), z_bar_matrix(A)
    lam = sp.expand(z * z.conjugate())
    lam_bar = sp.expand(zb * zb.conjugate())
    assert _zero(lam_bar - METRIC * lam.T * METRIC)
    assert bonus_lambda_zbar_theorem()


def test_lt7_to_lt10_direct():
    """Independent re-statement of the four Σ̄ sandwiches: the SAME
    scalar factors as the Σ family (q̄ conjugate, q transpose)."""
    z, zb = z_matrix(A), z_bar_matrix(A)
    q = sp.expand(A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2)
    qc = sp.conjugate(q)
    for m in range(4):
        assert _zero(z.conjugate() * SIGMA_BAR[m] * zb.conjugate()
                     - qc * SIGMA_BAR[m])
        assert _zero(zb.conjugate() * SIGMA_BAR[m] * z.conjugate()
                     - qc * SIGMA_BAR[m])
        assert _zero(z.T * SIGMA_BAR[m] * zb.T - q * SIGMA_BAR[m])
        assert _zero(zb.T * SIGMA_BAR[m] * z.T - q * SIGMA_BAR[m])


# -- the guard-level mechanism behind the spec-mirror form -------------------------

def test_c_is_lambda_inverse_on_the_guard():
    """On q = 1, C = gΛᵀg is Λ⁻¹ (via ΛᵀgΛ = g): Λ·C = I exactly, for
    boost AND rotation. This is what turns LT6 into the spec-mirror
    Σ̄^μ = Λ^μ_ν Z Σ̄^ν Z† — the exact dual of Task-1's I1."""
    phi = sp.symbols("phi", real=True)
    th = sp.symbols("theta", real=True)
    for al in (boost_alpha(phi, (1, 0, 0)), rotation_alpha(th, (0, 0, 1))):
        z = z_matrix(al)
        lam = sp.expand(z * z.conjugate())
        c = sp.expand(METRIC * lam.T * METRIC)
        assert _exp_zero(sp.expand(lam * c) - sp.eye(4))


def test_c_lambda_product_guard_free_and_c_transpose():
    """|q|² sharpening (contributed by the L2 adversarial review, locked
    here at L3): C·Λ = Λ·C = q q̄ 𝕀 GUARD-FREE — the guard-level
    C = Λ⁻¹ above is its q = 1 corollary. Plus Cᵀ = gΛg: the gΛg
    negative pin doubles as the row/column-convention pin for C."""
    z = z_matrix(A)
    lam = sp.expand(z * z.conjugate())
    c = sp.expand(METRIC * lam.T * METRIC)
    q = A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2
    qq = sp.expand(q * sp.conjugate(q))
    assert _zero(sp.expand(c * lam) - qq * sp.eye(4))
    assert _zero(sp.expand(lam * c) - qq * sp.eye(4))
    assert sp.expand(c.T - METRIC * lam * METRIC) == sp.zeros(4)


# -- the spec-mirror forms on the guard (boosts AND rotations) ---------------------

@pytest.mark.parametrize("which", ["J1", "J2", "J3", "J4", "J5"])
def test_spec_mirror_forms_hold_for_boost_and_rotation(which):
    phi = sp.symbols("phi", real=True)
    th = sp.symbols("theta", real=True)
    assert spec_form_holds_bar(boost_alpha(phi, (1, 0, 0)), which)
    assert spec_form_holds_bar(rotation_alpha(th, (0, 0, 1)), which)


def test_spec_form_bar_guard_is_enforced():
    with pytest.raises(ValueError, match="guard"):
        spec_form_holds_bar((2, 0, 0, 0), "J2")     # q = 4 != 1
    with pytest.raises(ValueError, match="which"):
        spec_form_holds_bar((1, 0, 0, 0), "J9")
