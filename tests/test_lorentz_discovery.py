"""Milestone L5 (FROZEN-7): the discovery sweep — Task 3 on the
declared 128-sandwich space, completed.

One exact symbolic sweep (module-scoped fixture; ~2 min) backs the
completeness claims; the individual statement tests are independent
direct proofs that do not go through the sweep machinery.
"""
import json
import pathlib

import pytest
import sympy as sp

from organon_mueller.lorentz import METRIC, z_bar_matrix, z_matrix
from organon_mueller.lorentz.discovery import (
    PAIR_NAMES,
    full_sweep,
    sweep_report,
)
from organon_mueller.lorentz.terms import (
    KNOWN_TEN,
    classify_all,
    letter_matrices,
)

A = sp.symbols("e0 e1 e2 e3", complex=True)
ROOT = pathlib.Path(__file__).resolve().parent.parent


def _zero(m):
    return sp.expand(m) == sp.zeros(4)


@pytest.fixture(scope="module")
def sweep():
    return full_sweep()


def test_completeness_partition(sweep):
    """THE COMPLETENESS THEOREM of the declared space: every sandwich
    is either a proven identity or a certified non-identity."""
    assert len(sweep) == 128
    kinds = {}
    for kind, _, _ in sweep.values():
        kinds[kind] = kinds.get(kind, 0) + 1
    assert kinds == {"identity": 40, "no-expansion": 88}


def test_lambda_family_closure_eight_members(sweep):
    """LT1/LT6 sit inside an 8-member Λ-family (6 NEW theorems at L5):
    each family member's coefficient matrix IS the stated Λ-form
    (asserted at the matrix level, not by name; matrices built from
    the sweep's own library so symbols line up)."""
    _, _, bases = _sweep_library()
    lam, lamb = bases["Z.Zc"], bases["Zb.Zbc"]
    family = {
        ("Zd", "S", "Z"): lam, ("Z", "S", "Zd"): lam.T,
        ("Zbd", "S", "Zb"): lamb, ("Zb", "S", "Zbd"): lamb.T,
        ("Z", "Sb", "Zd"): lamb, ("Zd", "Sb", "Z"): lamb.T,
        ("Zb", "Sb", "Zbd"): lam, ("Zbd", "Sb", "Zb"): lam.T,
    }
    for key, want in family.items():
        kind, s, b = sweep[key]
        assert kind == "identity" and s == "1", (key, kind, s, b)
        assert _zero(bases[b] - want), (key, b)


def _sweep_library():
    from organon_mueller.lorentz.discovery import _library
    return _library()


def test_second_kind_statements_direct():
    """Direct proofs (no sweep machinery): the ZZᵀ-type identities —
    Z Σ^μ Z = (ZZᵀ)^μ_ν Σ^ν and its bar/mixed relatives."""
    from organon_mueller.lorentz import SIGMA, SIGMA_BAR
    L = letter_matrices(A)
    cases = [
        ("Z", SIGMA, "Z", sp.expand(L["Z"] * L["Zt"])),
        ("Z", SIGMA, "Zb", sp.expand(L["Zt"] * L["Zb"])),
        ("Zb", SIGMA_BAR, "Zb", sp.expand(L["Z"] * L["Zt"])),
    ]
    for xn, fam, yn, C in cases:
        for m in range(4):
            rhs = sum((C[m, n] * sp.Matrix(fam[n]) for n in range(4)),
                      sp.zeros(4))
            assert _zero(L[xn] * sp.Matrix(fam[m]) * L[yn] - rhs)


def test_canonical_order_rule_is_needed_and_applied(sweep):
    """Degenerate pairs exist (Z·Z̄ = q·I — proven here), so canonical
    order matters: degenerate coefficient matrices must be named via
    I, never via a pair."""
    L = letter_matrices(A)
    q = A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2
    assert _zero(sp.expand(L["Z"] * L["Zb"]) - q * sp.eye(4))
    for key, want_s in ((("Zc", "S", "Zbc"), "qbar"),
                        (("Zt", "S", "Zbt"), "q")):
        kind, s, b = sweep[key]
        assert (kind, s, b) == ("identity", want_s, "I"), (key, s, b)
    assert PAIR_NAMES[0] == "I"


def test_negative_set_matches_the_l4_numeric_screen(sweep):
    """Cross-layer consistency: the sweep's SYMBOLIC negative set is
    exactly the L4 numeric screen's no-expansion set (both directions
    — the screen missed nothing and invented nothing)."""
    numeric = classify_all()
    sym_neg = {k for k, (kind, _, _) in sweep.items()
               if kind == "no-expansion"}
    num_neg = {k for k, (kind, _) in numeric.items()
               if kind == "no-expansion"}
    assert sym_neg == num_neg
    sym_id = {k for k, (kind, _, _) in sweep.items()
              if kind == "identity"}
    num_exp = {k for k, (kind, _) in numeric.items()
               if kind != "no-expansion"}
    assert sym_id == num_exp


def test_l4_crosswalk_the_sixteen_matches(sweep):
    """Every L4 match reappears in the sweep as an identity with a
    consistent class: same scalar; base I stays I, Λ-form names map to
    equal matrices."""
    _, _, bases = _sweep_library()
    lam, lamb = bases["Z.Zc"], bases["Zb.Zbc"]
    l4_bases = {"I": sp.eye(4), "Lam": lam, "LamT": lam.T,
                "Lambar": lamb, "LambarT": lamb.T}
    numeric = classify_all()
    l4_matches = {k: v for k, (kind, v) in numeric.items()
                  if kind == "match"}
    assert len(l4_matches) == 16
    for key, (s4, b4) in l4_matches.items():
        kind, s5, b5 = sweep[key]
        assert kind == "identity" and s5 == s4, (key, s4, s5)
        assert _zero(bases[b5] - l4_bases[b4]), (key, b4, b5)


def test_falsified_conjecture_pins():
    """HONEST RECORD: the tempting structural lemmas are FALSE —
    Σ̄¹ ≠ gΣ¹g and Z̄ ≠ gZg (the i-carrying entries do not flip).
    Probe 2 falsified them before any claim was made; locked here so
    they cannot sneak back in."""
    from organon_mueller.lorentz import SIGMA, SIGMA_BAR
    g = sp.Matrix(METRIC)
    assert sp.expand(sp.Matrix(SIGMA_BAR[1]) - g * sp.Matrix(SIGMA[1])
                     * g) != sp.zeros(4)
    z, zb = z_matrix(A), z_bar_matrix(A)
    assert sp.expand(zb - g * z * g) != sp.zeros(4)


def test_committed_report_is_reproducible(sweep):
    """The committed reports/sweep-lorentz-01.json is exactly what the
    engine regenerates (deterministic-report tradition; also pins the
    novelty boundary sentence into the artifact)."""
    committed = json.loads((ROOT / "reports" / "sweep-lorentz-01.json")
                           .read_text(encoding="utf-8"))
    regenerated = sweep_report(sweep)
    assert committed == regenerated
    assert "novelty NOT claimed" in committed["evidence"]
    assert committed["counts"] == {"identities": 40,
                                   "no_expansion": 88, "total": 128}
