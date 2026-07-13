"""Stage-7: the Sum/Scale language extension — acceptance targets from
docs/design-note-addition-scalars.md, soundness properties, fingerprint
scale-relativity, and K11 sentinels for the old language."""
import numpy as np
import pytest

pytest.importorskip("egglog")

from organon_mueller.discovery.engine import DiscoveryEngine  # noqa: E402
from organon_mueller.discovery.fingerprint import (  # noqa: E402
    bucket_by_fingerprint,
    fingerprint_key,
)
from organon_mueller.discovery.interpret import (  # noqa: E402
    random_assignment,
    terms_numerically_equal,
)
from organon_mueller.discovery.recovery import (  # noqa: E402
    _I15_CROSS,
    _I15_LHS,
    _I15_RHS,
)
from organon_mueller.discovery.symbolic import terms_symbolically_equal  # noqa: E402
from organon_mueller.discovery.terms import (  # noqa: E402
    Atom,
    Conj,
    Mul,
    Scale,
    ScalarAtom,
    ScalarConj,
    Sum,
    enumerate_extended,
    enumerate_terms,
)

A, B = Atom("a"), Atom("b")
P, Q = ScalarAtom("p"), ScalarAtom("q")
ATOMS, SCALARS = ("a", "b"), ("p", "q")

_ENGINE = DiscoveryEngine(atom_names=ATOMS, scalar_names=SCALARS)


# -- acceptance A/B (design note) --------------------------------------------

def test_acceptance_a_i15_expansion():
    """(pZa+qZb)·conj(pZa+qZb) == 4-term nested-Scale expansion — PROVEN."""
    assert _ENGINE.provable(_I15_LHS, _I15_RHS)
    assert terms_symbolically_equal(_I15_LHS, _I15_RHS, ATOMS, scalar_names=SCALARS)
    assert terms_numerically_equal(_I15_LHS, _I15_RHS, ATOMS, scalar_names=SCALARS)


def test_acceptance_b_i15_cross_term_reality():
    """Cross term equals its own conj — real for ALL coefficients (M26)."""
    assert _ENGINE.provable(_I15_CROSS, Conj(_I15_CROSS))
    assert terms_symbolically_equal(
        _I15_CROSS, Conj(_I15_CROSS), ATOMS, scalar_names=SCALARS
    )


# -- soundness of the new axioms ----------------------------------------------

def test_new_axioms_numeric_soundness_samples():
    """Each design-note rule instance holds numerically (spot instances)."""
    cases = [
        (Sum(A, B), Sum(B, A)),
        (Mul(A, Sum(B, Conj(A))), Sum(Mul(A, B), Mul(A, Conj(A)))),
        (Conj(Sum(A, B)), Sum(Conj(A), Conj(B))),
        (Conj(Scale(P, A)), Scale(ScalarConj(P), Conj(A))),
        (Mul(Scale(P, A), B), Scale(P, Mul(A, B))),
        (Mul(A, Scale(P, B)), Scale(P, Mul(A, B))),
        (Scale(P, Scale(Q, A)), Scale(Q, Scale(P, A))),
        # scale-over-sum (auditor-approved post-review addition, K24)
        (Scale(P, Sum(A, B)), Sum(Scale(P, A), Scale(P, B))),
    ]
    for left, right in cases:
        assert _ENGINE.provable(left, right), (left.render(), right.render())
        assert terms_numerically_equal(left, right, ATOMS, scalar_names=SCALARS)


def test_negative_controls_extended():
    """No invented equalities: sums/scales of distinct things stay distinct."""
    assert not _ENGINE.provable(Sum(A, B), Mul(A, B))
    assert not terms_numerically_equal(Sum(A, B), Mul(A, B), ATOMS, scalar_names=SCALARS)
    assert not _ENGINE.provable(Scale(P, A), Scale(Q, A))
    assert not terms_numerically_equal(
        Scale(P, A), Scale(Q, A), ATOMS, scalar_names=SCALARS
    )
    # scalar conj matters: conj(p)·X != p·X generically
    assert not _ENGINE.provable(Scale(ScalarConj(P), A), Scale(P, A))
    assert not terms_numerically_equal(
        Scale(ScalarConj(P), A), Scale(P, A), ATOMS, scalar_names=SCALARS
    )


# -- fingerprint: scale-relative key -------------------------------------------

def test_fingerprint_zero_and_equal_keys():
    rng = np.random.default_rng(424242)
    assignment = random_assignment(ATOMS, rng, SCALARS)
    # truly equal terms share the key
    assert fingerprint_key(_I15_LHS, assignment) == fingerprint_key(
        _I15_RHS, assignment
    )
    # proportional terms MAY collide (expected, filtered downstream):
    # p·X vs X — normalized values differ only by phase of p; do not assert
    # either way, but the bucketing must still separate genuinely different terms
    buckets = bucket_by_fingerprint(
        [Sum(A, B), Mul(A, B), _I15_LHS, _I15_RHS], ATOMS, scalar_names=SCALARS
    )
    as_sets = [set(g) for g in buckets]
    assert {_I15_LHS, _I15_RHS} in as_sets
    assert {Sum(A, B)} in as_sets and {Mul(A, B)} in as_sets


# -- enumeration ----------------------------------------------------------------

def test_extended_enumeration_deterministic_and_bounded():
    first = enumerate_extended(ATOMS, SCALARS, 7)
    second = enumerate_extended(ATOMS, SCALARS, 7)
    assert first == second  # K12
    assert len(first) == len(set(first))
    assert all(t.size() <= 7 for t in first)

    def sum_count(t):
        if isinstance(t, Sum):
            return 1 + sum_count(t.left) + sum_count(t.right)
        if isinstance(t, Mul):
            return sum_count(t.left) + sum_count(t.right)
        if isinstance(t, (Conj, Scale)):
            return sum_count(t.arg)
        return 0

    assert all(sum_count(t) <= 1 for t in first)  # max_sums=1


def test_k11_old_language_untouched():
    """Sentinels: pre-stage-7 enumeration counts are byte-stable."""
    assert len(enumerate_terms(("a", "b"), 7)) == 570
    assert len(enumerate_terms(("a", "b"), 7, conj_normal=True)) == 212
    assert len(enumerate_terms(("a", "b"), 5, conj_normal=True)) == 36


def test_name_collision_guard():
    with pytest.raises(ValueError):
        DiscoveryEngine(atom_names=("a", "b"), scalar_names=("a",))
