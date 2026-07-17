"""Term language over the Lorentz-face alphabet + the self-recovery
gate (milestone L4, FROZEN-7).

Alphabet (8 letters, all polynomial in generic complex α — guard-free):
{Z, Z*, Zᵀ, Z†} × {plain, bar}. Inverse convention (M29-style):
Z⁻¹ = q⁻¹ Z̄, so inverses are covered by the bar letters up to the
scalar q; the alphabet deliberately has no denominators.

Sandwich space: X · mid^μ · Y, mid ∈ {Σ, Σ̄} — 128 sandwiches, the
exact shape family of the work order's Tasks 1–2.

Classifier (numeric, two fixed seeds, genuinely complex α):
trace-extract C in the mid family's own dual basis, demand the
expansion is exact, then match C against s·B with s ∈ {1, q, q̄, qq̄}
and B ∈ {I, Λ, Λᵀ, Λ̄, Λ̄ᵀ}. Base aliases (L2 bonus theorem, locked
in tests): Λ̄ = gΛᵀg and Λ̄ᵀ = gΛg — the g-conjugates are NOT
separate bases.

Certifier: a generic SYMBOLIC prover for any classified sandwich — a
code path independent of ``identities.py``'s per-theorem checks, so a
gate certification is a genuine re-derivation.

SELF-RECOVERY GATE (v2 A5 recovery-campaign tradition): the
enumeration + certifier must find and prove the ten known identities
THEMSELVES. The known list is consulted only in the VERDICT comparison
— never in the discovery or certification path.
"""
from __future__ import annotations

import numpy as np
import sympy as sp

from .core import SIGMA, SIGMA_BAR

__all__ = ["NAMES", "KNOWN_TEN", "SEEDS", "letter_matrices",
           "classify_all", "certify", "recovery_gate"]

NAMES = ("Z", "Zc", "Zt", "Zd", "Zb", "Zbc", "Zbt", "Zbd")
SEEDS = (20260716, 20260717)
_TOL = 1e-7

#: The ten known identities (LT1–LT10) in classifier vocabulary.
#: Used ONLY by the gate's verdict comparison — see module docstring.
KNOWN_TEN = {
    ("Zd", "S", "Z"): ("1", "Lam"),
    ("Zc", "S", "Zbc"): ("qbar", "I"),
    ("Zbc", "S", "Zc"): ("qbar", "I"),
    ("Zt", "S", "Zbt"): ("q", "I"),
    ("Zbt", "S", "Zt"): ("q", "I"),
    ("Z", "Sb", "Zd"): ("1", "Lambar"),
    ("Zc", "Sb", "Zbc"): ("qbar", "I"),
    ("Zbc", "Sb", "Zc"): ("qbar", "I"),
    ("Zt", "Sb", "Zbt"): ("q", "I"),
    ("Zbt", "Sb", "Zt"): ("q", "I"),
}

_SIG_N = [np.array(m, dtype=complex) for m in SIGMA]
_SIGB_N = [np.array(m, dtype=complex) for m in SIGMA_BAR]


def _eight(z, zb, conj, transpose):
    return dict(zip(NAMES, [
        z, conj(z), transpose(z), transpose(conj(z)),
        zb, conj(zb), transpose(zb), transpose(conj(zb)),
    ]))


def letter_matrices(alpha):
    """The 8 letters as exact sympy matrices at parameter vector
    ``alpha`` (symbols allowed)."""
    z = sum((alpha[m] * sp.Matrix(SIGMA[m]) for m in range(4)),
            sp.zeros(4))
    zb = sum((alpha[m] * sp.Matrix(SIGMA_BAR[m]) for m in range(4)),
             sp.zeros(4))
    return _eight(z, zb, lambda m: m.conjugate(), lambda m: m.T)


def _numeric_letters(a):
    z = sum(a[m] * _SIG_N[m] for m in range(4))
    zb = sum(a[m] * _SIGB_N[m] for m in range(4))
    return _eight(z, zb, np.conj, np.transpose)


def _candidates(a, L):
    q = a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2
    lam = L["Z"] @ L["Zc"]
    lamb = L["Zb"] @ L["Zbc"]
    bases = [("I", np.eye(4, dtype=complex)), ("Lam", lam),
             ("LamT", lam.T), ("Lambar", lamb), ("LambarT", lamb.T)]
    scalars = [("1", 1.0 + 0j), ("q", q), ("qbar", np.conj(q)),
               ("qqbar", q * np.conj(q))]
    return bases, scalars


def _classify_at(a):
    L = _numeric_letters(a)
    bases, scalars = _candidates(a, L)
    cand = [(sn, bn, s * B) for sn, s in scalars for bn, B in bases]
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            if np.linalg.norm(cand[i][2] - cand[j][2]) <= 1e-5:
                raise ValueError(
                    "candidate collision at this seed — classification "
                    "would be ambiguous; change seeds")
    out = {}
    for mid_name, fam in (("S", _SIG_N), ("Sb", _SIGB_N)):
        for xn in NAMES:
            for yn in NAMES:
                M = [L[xn] @ fam[m] @ L[yn] for m in range(4)]
                C = np.array([[np.trace(fam[n] @ M[m]) / 4
                               for n in range(4)] for m in range(4)])
                R = [sum(C[m, n] * fam[n] for n in range(4))
                     for m in range(4)]
                if max(np.linalg.norm(M[m] - R[m])
                       for m in range(4)) > _TOL:
                    out[(xn, mid_name, yn)] = ("no-expansion", None)
                    continue
                hit = next(((sn, bn) for sn, bn, sB in cand
                            if np.linalg.norm(C - sB) <= _TOL), None)
                out[(xn, mid_name, yn)] = \
                    ("match", hit) if hit else ("expansion-unmatched",
                                                None)
    return out


def classify_all(seeds=SEEDS):
    """Numeric classification of all 128 sandwiches; the fixed seeds
    must agree exactly (deterministic screen, no flakes)."""
    runs = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        a = rng.normal(size=4) + 1j * rng.normal(size=4)
        if abs(a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2) < 0.1:
            raise ValueError(f"seed {seed} lands too close to the null "
                             "cone; classification needs |q| bounded "
                             "away from 0")
        runs.append(_classify_at(a))
    if any(r != runs[0] for r in runs[1:]):
        raise ValueError("seeds disagree — numeric classification is "
                         "not trustworthy at this tolerance")
    return runs[0]


_A = sp.symbols("_tm_a0 _tm_a1 _tm_a2 _tm_a3", complex=True)


def certify(x: str, mid: str, y: str, scalar: str, base: str) -> bool:
    """SYMBOLIC certification (exact, guard-free, generic complex α):
    prove  X · mid^μ · Y  =  Σ_ν (s·B)^μ_ν · mid^ν  for all μ."""
    if mid not in ("S", "Sb"):
        raise ValueError("mid must be 'S' (Sigma) or 'Sb' (Sigma-bar)")
    L = letter_matrices(_A)
    if x not in L or y not in L:
        raise ValueError(f"letters must be in {NAMES}")
    fam = SIGMA if mid == "S" else SIGMA_BAR
    q = _A[0]**2 - _A[1]**2 - _A[2]**2 - _A[3]**2
    scalars = {"1": sp.Integer(1), "q": q, "qbar": sp.conjugate(q),
               "qqbar": sp.expand(q * sp.conjugate(q))}
    lam = sp.expand(L["Z"] * L["Zc"])
    lamb = sp.expand(L["Zb"] * L["Zbc"])
    bases = {"I": sp.eye(4), "Lam": lam, "LamT": lam.T,
             "Lambar": lamb, "LambarT": lamb.T}
    if scalar not in scalars or base not in bases:
        raise ValueError(f"scalar must be in {sorted(scalars)}, "
                         f"base in {sorted(bases)}")
    sB = sp.expand(scalars[scalar] * bases[base])
    return all(
        sp.expand(L[x] * fam[m] * L[y]
                  - sum((sB[m, n] * fam[n] for n in range(4)),
                        sp.zeros(4))) == sp.zeros(4)
        for m in range(4))


def recovery_gate() -> dict:
    """The self-recovery gate: enumerate (numeric, registry-blind),
    then symbolically certify every KNOWN_TEN entry through the
    generic certifier. PASS iff all ten are found with their exact
    classes AND all ten certifications prove."""
    cls = classify_all()
    matches = {k: v for k, (kind, v) in cls.items() if kind == "match"}
    found = {k: matches.get(k) == v for k, v in KNOWN_TEN.items()}
    certified = {k: certify(k[0], k[1], k[2], *v)
                 for k, v in KNOWN_TEN.items()}
    counts = {}
    for kind, _ in cls.values():
        counts[kind] = counts.get(kind, 0) + 1
    return {
        "passed": all(found.values()) and all(certified.values()),
        "found": found,
        "certified": certified,
        "class_counts": counts,
        "extra_matches": sorted(k for k in matches if k not in
                                KNOWN_TEN),
    }
