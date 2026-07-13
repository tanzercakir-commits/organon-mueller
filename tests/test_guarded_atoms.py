"""Stage-9(b): guarded atoms — constrained generators, faithfulness
obligations, and the first populated underivable-style channel output
(Horn-conditional identity candidates, M32)."""
import numpy as np
import pytest

pytest.importorskip("egglog")

import sympy as sp  # noqa: E402

from organon_mueller.conditions import is_hermitian_state, is_unitary_state  # noqa: E402
from organon_mueller.discovery.guards import (  # noqa: E402
    GUARD_KEYS,
    GuardedAtom,
    guarded_random_hvector,
    guarded_symbolic_hvector,
    guarded_numerically_equal,
    guarded_symbolically_equal,
    run_guarded_campaign,
)
from organon_mueller.discovery.terms import Atom, Mul  # noqa: E402


# -- generator faithfulness (stage-8 design-note obligation 1) -----------------

def test_numeric_generators_satisfy_their_predicates():
    rng = np.random.default_rng(20260713)
    for _ in range(10):
        hv = guarded_random_hvector(rng, "hermitian_state")
        assert is_hermitian_state([hv.tau, hv.alpha, hv.beta, hv.gamma])
        hv = guarded_random_hvector(rng, "unitary_state")
        assert is_unitary_state([hv.tau, hv.alpha, hv.beta, hv.gamma])
        hv = guarded_random_hvector(rng, "class2_ta")
        assert hv.beta == 0 and hv.gamma == 0 and hv.tau != 0
        hv = guarded_random_hvector(rng, "class2_tb")
        assert hv.alpha == 0 and hv.gamma == 0
        hv = guarded_random_hvector(rng, "class2_tg")
        assert hv.alpha == 0 and hv.beta == 0


def test_symbolic_generators_generic_and_faithful():
    # hermitian: 4 independent REAL symbols; conjugation acts trivially
    hv = guarded_symbolic_hvector("x", "hermitian_state")
    syms = hv.to_z().free_symbols
    assert len(syms) == 4 and all(s.is_real for s in syms)
    # unitary: tau real, vector part I*(real) — conj flips the vector part
    hv = guarded_symbolic_hvector("x", "unitary_state")
    assert sp.simplify(sp.conjugate(hv.alpha) + hv.alpha) == 0
    assert sp.simplify(sp.conjugate(hv.tau) - hv.tau) == 0
    # class2: exactly two complex parameters, right slots zeroed
    hv = guarded_symbolic_hvector("x", "class2_ta")
    assert hv.beta == 0 and hv.gamma == 0
    assert len(hv.to_z().free_symbols) == 2
    # independence across names (K17)
    a = guarded_symbolic_hvector("a", "class2_ta").to_z().free_symbols
    b = guarded_symbolic_hvector("b", "class2_ta").to_z().free_symbols
    assert not (a & b)


def test_guard_keys_registered():
    from organon_mueller.conditions import CONDITIONS

    # guard vocabulary must stay within (or extend) the CONDITIONS keys
    for key in ("hermitian_state", "unitary_state"):
        assert key in CONDITIONS
    assert set(GUARD_KEYS) >= {"class2_ta", "class2_tb", "class2_tg"}


# -- the first Horn-conditional identity candidates (M32) -----------------------

def test_guarded_campaign_first_conditional_identities():
    findings = run_guarded_campaign()
    assert len(findings) == 3  # class2_ta, class2_tb, class2_tg (review sug. 2)
    for f in findings:
        assert f.symbolic_guarded, f"guarded exact proof failed: {f.left.render()}"
        assert f.numeric_guarded
        assert not f.provable_unguarded  # axioms are guard-blind
        assert not f.symbolic_unguarded  # genuinely conditional (M32)
        assert f.is_conditional_identity


def test_mixed_guards_negative_control():
    """class2_ta x class2_tg does NOT commute — the guard label must not
    leak across classes (probe-verified before implementation)."""
    a = GuardedAtom("a", guard="class2_ta")
    b = GuardedAtom("b", guard="class2_tg")
    guards = {"a": "class2_ta", "b": "class2_tg"}
    assert not guarded_symbolically_equal(Mul(a, b), Mul(b, a), guards)
    assert not guarded_numerically_equal(Mul(a, b), Mul(b, a), guards)


def test_guarded_atom_is_atom_but_distinct():
    plain, guarded = Atom("a"), GuardedAtom("a", guard="class2_ta")
    assert isinstance(guarded, Atom)
    assert guarded != plain  # dataclass eq is class-aware
    assert guarded.render() == "a{class2_ta}"
