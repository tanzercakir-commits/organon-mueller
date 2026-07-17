"""Discovery sweep over the Lorentz-face sandwich space (milestone L5,
FROZEN-7) — the work order's Task 3, restricted to the declared space.

Exact end-to-end (no seeds, no numerics): for every one of the 128
sandwiches X·mid^μ·Y over the 8-letter alphabet, either

- an IDENTITY is proven: X mid^μ Y = Σ_ν (s·B)^μ_ν mid^ν with
  s ∈ {1, q, q̄, qq̄} and B ∈ {I} ∪ {all 64 ordered two-letter
  products}, or
- a NEGATIVE CERTIFICATE is proven: the residual after projecting on
  the mid family's dual basis is a nonzero polynomial in α — no
  expansion in the mid family exists.

CANONICAL NAMING RULE: candidates are tried in a documented order —
I first (all four scalars), then the 64 pairs in alphabet order (each
with all four scalars). Needed because degenerate pairs exist
(Z·Z̄ = q·I): C = q·I must be reported as ("q", "I"), never as
("1", "Z.Zb"). The first hit in canonical order is THE name.

FALSIFIED-CONJECTURE RECORD (honest, locked by tests): the tempting
lemmas Σ̄^μ = gΣ^μg and Z̄ = gZg are FALSE — the i-carrying entries
of Σ¹/Σ³ do not flip under g-conjugation. A family-swap channel built
on them found zero matches in probe 2; it is therefore NOT part of
this module.

Novelty boundary: every statement here is evidence class
symbolic-proof AS AN IDENTITY; novelty relative to the literature is
deliberately not claimed (human judgement — collaborator report #2).
"""
from __future__ import annotations

import sympy as sp

from .core import SIGMA, SIGMA_BAR
from .terms import NAMES, letter_matrices

__all__ = ["PAIR_NAMES", "full_sweep", "sweep_report"]

_A = sp.symbols("_dv_a0 _dv_a1 _dv_a2 _dv_a3", complex=True)

#: Canonical candidate order: I first, then ordered pairs "X.Y".
PAIR_NAMES = ("I",) + tuple(f"{x}.{y}" for x in NAMES for y in NAMES)


def _zero(m):
    return sp.expand(m) == sp.zeros(4)


def _library():
    L = letter_matrices(_A)
    q = _A[0]**2 - _A[1]**2 - _A[2]**2 - _A[3]**2
    scalars = (("1", sp.Integer(1)), ("q", q),
               ("qbar", sp.conjugate(q)),
               ("qqbar", sp.expand(q * sp.conjugate(q))))
    bases = {"I": sp.eye(4)}
    for x in NAMES:
        for y in NAMES:
            bases[f"{x}.{y}"] = sp.expand(L[x] * L[y])
    return L, scalars, bases


def full_sweep() -> dict:
    """Classify all 128 sandwiches exactly. Returns
    {(x, mid, y): ("identity", scalar_name, base_name) |
                  ("no-expansion", None, None)}."""
    L, scalars, bases = _library()
    out = {}
    for mid_name, fam_raw in (("S", SIGMA), ("Sb", SIGMA_BAR)):
        fam = [sp.Matrix(f) for f in fam_raw]
        for xn in NAMES:
            for yn in NAMES:
                M = [sp.expand(L[xn] * fam[m] * L[yn])
                     for m in range(4)]
                C = sp.Matrix(4, 4, lambda m, n: sp.expand(
                    sp.trace(fam[n] * M[m]) / 4))
                recon_ok = all(
                    _zero(M[m] - sum((C[m, n] * fam[n]
                                      for n in range(4)), sp.zeros(4)))
                    for m in range(4))
                if not recon_ok:
                    out[(xn, mid_name, yn)] = ("no-expansion", None,
                                               None)
                    continue
                hit = None
                for b_name in PAIR_NAMES:          # canonical order
                    B = bases[b_name]
                    for s_name, s in scalars:
                        if _zero(C - sp.expand(s * B)):
                            hit = (s_name, b_name)
                            break
                    if hit:
                        break
                if hit is None:                    # pragma: no cover
                    raise RuntimeError(
                        f"sweep hole: ({xn},{mid_name},{yn}) expands "
                        "but no canonical candidate matches — the "
                        "completeness theorem would be false; report "
                        "this sandwich")
                out[(xn, mid_name, yn)] = ("identity",) + hit
    return out


def sweep_report(sweep: dict | None = None) -> dict:
    """Deterministic JSON-able report of the full sweep (engine report
    tradition: sorted keys, counts first, no timestamps)."""
    sweep = full_sweep() if sweep is None else sweep
    identities = {f"{x} {mid} {y}": [s, b]
                  for (x, mid, y), (kind, s, b) in sorted(sweep.items())
                  if kind == "identity"}
    negatives = [f"{x} {mid} {y}"
                 for (x, mid, y), (kind, _, _) in sorted(sweep.items())
                 if kind == "no-expansion"]
    return {
        "space": "X mid Y; X,Y in 8-letter alphabet; mid in {S, Sb}",
        "alphabet": list(NAMES),
        "evidence": "symbolic-proof (exact, guard-free, generic "
                    "complex alpha); novelty NOT claimed",
        "counts": {"identities": len(identities),
                   "no_expansion": len(negatives), "total": 128},
        "identities": identities,
        "no_expansion": negatives,
    }
