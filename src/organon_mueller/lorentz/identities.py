"""Task-1 identities of the work order, proven as guard-free theorems
(milestone L1, FROZEN-7).

The work order states five identities (its Task 1), written with Z⁻¹ and
expected to hold "for both boosts and rotations", with a warning that
sign differences are conventions. L1's finding is stronger and cleaner:

**Each identity is the q = 1 corollary of a GUARD-FREE theorem** over
generic complex α (q ≡ α·α = α₀²−α₁²−α₂²−α₃², Z̄ = α_μΣ̄^μ):

  LT1:  Z† Σ^μ Z        = Λ^μ_ν Σ^ν          (Λ = ZZ*, ROW convention)
  LT2:  Z* Σ^μ Z̄*      = q̄ Σ^μ
  LT3:  Z̄* Σ^μ Z*      = q̄ Σ^μ
  LT4:  Z^T Σ^μ Z̄^T    = q Σ^μ
  LT5:  Z̄^T Σ^μ Z^T    = q Σ^μ
  chain: Λ(Z)·Λ(Z̄)     = q q̄ · I           (turns LT1 into spec-I1)

On the guard q = 1 — which boosts AND rotations both satisfy by
construction — Z⁻¹ = Z̄ and q = q̄ = 1, so the spec's five identities
hold EXACTLY AS WRITTEN, for boosts and rotations alike.

SIGN-CONVENTION TABLE (the spec's warning, resolved for OUR
parametrizations — recorded M29-style):

  identity   boost      rotation    convention that must be pinned
  I1         as-written as-written  Λ^μ_ν = Λ[row μ][col ν]; the COLUMN
                                    form is FALSE (locked by a test)
  I2–I5      as-written as-written  none — no sign flip needed
  (lemma)                           Z(α)* = Z(α*)ᵀ (guard-free; Σ* = Σᵀ);
                                    at the PARAMETER level conjugation
                                    reverses rotations (α_rot(θ)* =
                                    α_rot(−θ)) and fixes boosts — which
                                    is where parameter-sign freedom
                                    enters other parametrization
                                    choices.

Proof-engineering note (honest record): the first symbolic check of the
spec forms for boost/rotation returned a FALSE negative — a half-angle
hyperbolic SIMPLIFICATION weakness, not mathematics. Numerics disagreed,
and rewriting in exponentials (`rewrite(exp)`) proves exact zero. The
lesson is encoded in `_spec_zero`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import sympy as sp

from .core import (SIGMA, SIGMA_BAR, minkowski_square,
                   z_bar_matrix, z_matrix)

__all__ = ["LorentzIdentity", "LORENTZ_TASK1", "LORENTZ_TASK2",
           "verify_task1", "verify_task2", "spec_form_holds",
           "spec_form_holds_bar", "bonus_lambda_zbar_theorem"]

_A = sp.symbols("_lt_a0 _lt_a1 _lt_a2 _lt_a3", complex=True)


def _zero(m: sp.Matrix) -> bool:
    return sp.expand(m) == sp.zeros(4)


def _spec_zero(m: sp.Matrix) -> bool:
    """Zero test robust for half-angle hyperbolic/trig content (probe
    lesson: expand alone can false-negative; exponentials decide)."""
    return sp.simplify(sp.expand(m.rewrite(sp.exp))) == sp.zeros(4)


def _ctx():
    z, zb = z_matrix(_A), z_bar_matrix(_A)
    return z, zb, minkowski_square(_A)


@dataclass(frozen=True)
class LorentzIdentity:
    key: str
    statement: str            # the guard-free theorem
    spec_form: str            # as written in the work order (q = 1)
    check: Callable[[], bool]


def _lt1() -> bool:
    z, _, _ = _ctx()
    zd, lam = z.conjugate().T, sp.expand(z * z.conjugate())
    return all(_zero(zd * SIGMA[m] * z
                     - sum((lam[m, n] * SIGMA[n] for n in range(4)),
                           sp.zeros(4)))
               for m in range(4))


def _lt2() -> bool:
    z, zb, q = _ctx()
    return all(_zero(z.conjugate() * SIGMA[m] * zb.conjugate()
                     - sp.conjugate(q) * SIGMA[m]) for m in range(4))


def _lt3() -> bool:
    z, zb, q = _ctx()
    return all(_zero(zb.conjugate() * SIGMA[m] * z.conjugate()
                     - sp.conjugate(q) * SIGMA[m]) for m in range(4))


def _lt4() -> bool:
    z, zb, q = _ctx()
    return all(_zero(z.T * SIGMA[m] * zb.T - q * SIGMA[m])
               for m in range(4))


def _lt5() -> bool:
    z, zb, q = _ctx()
    return all(_zero(zb.T * SIGMA[m] * z.T - q * SIGMA[m])
               for m in range(4))


LORENTZ_TASK1 = (
    LorentzIdentity(
        "LT1", "Zdag S^mu Z = Lambda^mu_nu S^nu (Lambda=ZZ*, row conv.)",
        "S^mu = Lambda^mu_nu (Z^-1)dag S^nu Z^-1", _lt1),
    LorentzIdentity(
        "LT2", "Z* S^mu Zbar* = conj(q) S^mu",
        "S^mu = Z* S^mu (Z^-1)*", _lt2),
    LorentzIdentity(
        "LT3", "Zbar* S^mu Z* = conj(q) S^mu",
        "S^mu = (Z^-1)* S^mu Z*", _lt3),
    LorentzIdentity(
        "LT4", "Z^T S^mu Zbar^T = q S^mu",
        "S^mu = Z^T S^mu (Z^-1)^T", _lt4),
    LorentzIdentity(
        "LT5", "Zbar^T S^mu Z^T = q S^mu",
        "S^mu = (Z^-1)^T S^mu Z^T", _lt5),
)


def verify_task1() -> dict:
    """Prove all five guard-free theorems (exact symbolic)."""
    return {e.key: e.check() for e in LORENTZ_TASK1}


def spec_form_holds(alpha, which: str) -> bool:
    """Check one of the work order's identities AS WRITTEN for a concrete
    parametrization whose Minkowski square is 1 (so Z⁻¹ = Z̄): which in
    {'I1'..'I5'}. Exact symbolic (exp-rewrite robust)."""
    z, zb = z_matrix(alpha), z_bar_matrix(alpha)
    if sp.simplify(minkowski_square(alpha) - 1) != 0:
        raise ValueError("alpha must satisfy the guard alpha.alpha = 1 "
                         "for the spec forms (Z^-1 = Zbar)")
    lam = sp.expand(z * z.conjugate())
    forms = {
        "I1": lambda m: sum((lam[m, n] * (zb.conjugate().T) * SIGMA[n]
                             * zb for n in range(4)), sp.zeros(4)),
        "I2": lambda m: z.conjugate() * SIGMA[m] * zb.conjugate(),
        "I3": lambda m: zb.conjugate() * SIGMA[m] * z.conjugate(),
        "I4": lambda m: z.T * SIGMA[m] * zb.T,
        "I5": lambda m: zb.T * SIGMA[m] * z.T,
    }
    if which not in forms:
        raise ValueError(f"which must be one of {sorted(forms)}")
    f = forms[which]
    return all(_spec_zero(f(m) - SIGMA[m]) for m in range(4))


# ---------------------------------------------------------------- Task 2

def _lt6() -> bool:
    """Λ-type Σ̄ identity: Z Σ̄^μ Z† = C^μ_ν Σ̄^ν with C = gΛᵀg = Λ(Z̄).
    (The equality of the two identifications is the bonus theorem below.)"""
    from .core import METRIC

    z, zb, _ = _ctx()
    zd, lam = z.conjugate().T, sp.expand(z * z.conjugate())
    c = sp.expand(METRIC * lam.T * METRIC)
    return all(_zero(z * SIGMA_BAR[m] * zd
                     - sum((c[m, n] * SIGMA_BAR[n] for n in range(4)),
                           sp.zeros(4)))
               for m in range(4))


def _lt7() -> bool:
    z, zb, q = _ctx()
    return all(_zero(z.conjugate() * SIGMA_BAR[m] * zb.conjugate()
                     - sp.conjugate(q) * SIGMA_BAR[m]) for m in range(4))


def _lt8() -> bool:
    z, zb, q = _ctx()
    return all(_zero(zb.conjugate() * SIGMA_BAR[m] * z.conjugate()
                     - sp.conjugate(q) * SIGMA_BAR[m]) for m in range(4))


def _lt9() -> bool:
    z, zb, q = _ctx()
    return all(_zero(z.T * SIGMA_BAR[m] * zb.T - q * SIGMA_BAR[m])
               for m in range(4))


def _lt10() -> bool:
    z, zb, q = _ctx()
    return all(_zero(zb.T * SIGMA_BAR[m] * z.T - q * SIGMA_BAR[m])
               for m in range(4))


def bonus_lambda_zbar_theorem() -> bool:
    """BONUS (found while identifying LT6's coefficient matrix):
    Λ(Z̄) = g Λ(Z)ᵀ g, guard-free. On the guard this is Λ(Z̄) = Λ⁻¹
    (via Λᵀ g Λ = g), which turns LT6 into the spec-mirror form
    Σ̄^μ = Λ^μ_ν Z Σ̄^ν Z†."""
    from .core import METRIC

    z, zb, _ = _ctx()
    lam = sp.expand(z * z.conjugate())
    lam_bar = sp.expand(zb * zb.conjugate())
    return _zero(lam_bar - METRIC * lam.T * METRIC)


LORENTZ_TASK2 = (
    LorentzIdentity(
        "LT6", "Z Sbar^mu Zdag = (g Lambda^T g)^mu_nu Sbar^nu "
               "(= Lambda(Zbar)^mu_nu Sbar^nu)",
        "Sbar^mu = Lambda^mu_nu Z Sbar^nu Zdag", _lt6),
    LorentzIdentity(
        "LT7", "Z* Sbar^mu Zbar* = conj(q) Sbar^mu",
        "Sbar^mu = Z* Sbar^mu (Z^-1)*", _lt7),
    LorentzIdentity(
        "LT8", "Zbar* Sbar^mu Z* = conj(q) Sbar^mu",
        "Sbar^mu = (Z^-1)* Sbar^mu Z*", _lt8),
    LorentzIdentity(
        "LT9", "Z^T Sbar^mu Zbar^T = q Sbar^mu",
        "Sbar^mu = Z^T Sbar^mu (Z^-1)^T", _lt9),
    LorentzIdentity(
        "LT10", "Zbar^T Sbar^mu Z^T = q Sbar^mu",
        "Sbar^mu = (Z^-1)^T Sbar^mu Z^T", _lt10),
)


def verify_task2() -> dict:
    """Prove the five Σ̄ theorems (exact symbolic)."""
    return {e.key: e.check() for e in LORENTZ_TASK2}


def spec_form_holds_bar(alpha, which: str) -> bool:
    """The Task-2 spec-mirror forms AS WRITTEN, for a parametrization on
    the guard α·α = 1: which in {'J1'..'J5'} mirroring I1..I5 with Σ̄ in
    the middle (J1 uses the Λ^μ_ν Z Σ̄^ν Z† dual sandwich)."""
    z, zb = z_matrix(alpha), z_bar_matrix(alpha)
    if sp.simplify(minkowski_square(alpha) - 1) != 0:
        raise ValueError("alpha must satisfy the guard alpha.alpha = 1 "
                         "for the spec forms (Z^-1 = Zbar)")
    lam = sp.expand(z * z.conjugate())
    zd = z.conjugate().T
    forms = {
        "J1": lambda m: sum((lam[m, n] * z * SIGMA_BAR[n] * zd
                             for n in range(4)), sp.zeros(4)),
        "J2": lambda m: z.conjugate() * SIGMA_BAR[m] * zb.conjugate(),
        "J3": lambda m: zb.conjugate() * SIGMA_BAR[m] * z.conjugate(),
        "J4": lambda m: z.T * SIGMA_BAR[m] * zb.T,
        "J5": lambda m: zb.T * SIGMA_BAR[m] * z.T,
    }
    if which not in forms:
        raise ValueError(f"which must be one of {sorted(forms)}")
    f = forms[which]
    return all(_spec_zero(f(m) - SIGMA_BAR[m]) for m in range(4))
