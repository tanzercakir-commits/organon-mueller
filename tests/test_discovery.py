"""Stage-02/03 acceptance: the engine must REDISCOVER known structure
(R1-R3), must NOT invent commutativity (negative controls), and every
verified pair is the intersection of e-graph proof and independent numeric
verification (pipeline v1.1: isolated per-pair proof graphs, decision M18).
"""
import pytest

egglog = pytest.importorskip("egglog")  # decision M13: optional extra

from organon_mueller.discovery.engine import DiscoveryEngine  # noqa: E402
from organon_mueller.discovery.fingerprint import (  # noqa: E402
    FINGERPRINT_SEED,
    bucket_by_fingerprint,
)
from organon_mueller.discovery.interpret import terms_numerically_equal  # noqa: E402
from organon_mueller.discovery.terms import (  # noqa: E402
    Atom,
    Conj,
    Mul,
    enumerate_terms,
)
from organon_mueller.verify import DEFAULT_SEED  # noqa: E402

A, B = Atom("a"), Atom("b")
R2_LHS, R2_RHS = Mul(A, Conj(B)), Mul(Conj(B), A)
R3_LHS = Mul(Mul(A, B), Conj(Mul(A, B)))
R3_RHS = Mul(Mul(A, Conj(A)), Mul(B, Conj(B)))
# conj-normal form of R3's left side (pruned enumeration generates this one)
R3_LHS_NORMAL = Mul(Mul(A, B), Mul(Conj(A), Conj(B)))


@pytest.fixture(scope="module")
def engine() -> DiscoveryEngine:
    return DiscoveryEngine(atom_names=("a", "b"))


def test_enumeration_deterministic_and_sized():
    terms = enumerate_terms(("a", "b"), 7)
    assert terms == enumerate_terms(("a", "b"), 7)  # K12
    assert all(t.size() <= 7 for t in terms)
    assert len(terms) == len(set(terms))  # hashable, no duplicates
    assert R3_LHS.size() == 8 and R3_RHS.size() == 9  # documented correction


def test_conj_normal_enumeration_properties():
    def conj_ok(t) -> bool:
        if isinstance(t, Atom):
            return True
        if isinstance(t, Conj):
            return isinstance(t.arg, Atom)
        return conj_ok(t.left) and conj_ok(t.right)

    pruned = enumerate_terms(("a", "b"), 9, conj_normal=True)
    full = enumerate_terms(("a", "b"), 9)
    assert all(conj_ok(t) for t in pruned)
    assert set(pruned) <= set(full)
    assert len(pruned) < len(full) / 2  # meaningful pruning
    assert R3_LHS_NORMAL in pruned and R3_RHS in pruned


def test_fingerprint_seed_independent_of_verification():
    import inspect

    verification_seed = inspect.signature(
        terms_numerically_equal
    ).parameters["seed"].default
    assert FINGERPRINT_SEED != verification_seed  # K14, tied to actual default
    assert FINGERPRINT_SEED != DEFAULT_SEED


def test_fingerprint_buckets_group_known_equal_pairs():
    terms = [R2_LHS, R2_RHS, Mul(A, B), Mul(B, A)]
    buckets = bucket_by_fingerprint(terms, ("a", "b"))
    as_sets = [set(g) for g in buckets]
    assert {R2_LHS, R2_RHS} in as_sets            # equal pair lands together
    assert {Mul(A, B)} in as_sets and {Mul(B, A)} in as_sets  # unequal apart


def test_r1_conj_involution(engine):
    assert engine.provable(Conj(Conj(A)), A)


def test_r2_atom_commutation(engine):
    assert engine.provable(R2_LHS, R2_RHS)


def test_r3_serial_mueller_product(engine):
    """(a*b)*conj(a*b) == (a*conj(a)) * (b*conj(b))  — I10 consequence."""
    assert engine.provable(R3_LHS, R3_RHS)
    # and it is TRUE numerically, independent of the e-graph:
    assert terms_numerically_equal(R3_LHS, R3_RHS, ("a", "b"))


def test_negative_control_no_plain_commutativity(engine):
    assert not engine.provable(Mul(A, B), Mul(B, A))
    assert not terms_numerically_equal(Mul(A, B), Mul(B, A), ("a", "b"))


def test_negative_control_no_conj_conj_commutativity(engine):
    lhs, rhs = Mul(Conj(A), Conj(B)), Mul(Conj(B), Conj(A))
    assert not engine.provable(lhs, rhs)
    # indeed FALSE numerically, so the e-graph is right to keep them apart
    assert not terms_numerically_equal(lhs, rhs, ("a", "b"))


@pytest.mark.parametrize(
    "left,right",
    [
        # the {b, a, conj(a)} multiset family the shared-graph pipeline
        # wrongly left underivable (docs/egglog-large-graph-pathology.md)
        (Mul(B, Mul(A, Conj(A))), Mul(B, Mul(Conj(A), A))),
        (Mul(Mul(B, A), Conj(A)), Mul(B, Mul(Conj(A), A))),
        (Mul(Mul(B, Conj(A)), A), Mul(B, Mul(A, Conj(A)))),
        # and the mirrored {a, b, conj(b)} family
        (Mul(Mul(A, B), Conj(B)), Mul(A, Mul(Conj(B), B))),
        (Mul(Conj(A), Mul(A, B)), Mul(Mul(A, Conj(A)), B)),
        (Mul(Mul(B, Conj(B)), A), Mul(B, Mul(Conj(B), A))),
    ],
)
def test_pathology_family_now_proven(engine, left, right):
    assert engine.provable(left, right)
    assert terms_numerically_equal(left, right, ("a", "b"))


def test_full_run_pipeline_v1():
    result = DiscoveryEngine(
        atom_names=("a", "b"), max_size=9, conj_normal=True
    ).run()
    assert result.n_terms > 1000
    assert result.verified, "engine harvested no equivalences at all"
    assert result.sound, (
        "unsound axiom signal — refuted candidates: "
        + "; ".join(p.render() for p in result.refuted[:5])
    )
    harvested = {frozenset((p.left, p.right)) for p in result.verified}
    # I10 commutation rediscovered
    assert frozenset((R2_LHS, R2_RHS)) in harvested
    # serial Mueller product rediscovered in conj-normal form
    joined = {t for pair in harvested for t in pair}
    assert R3_RHS in joined and R3_LHS_NORMAL in joined
    # with isolated proofs the axioms are complete for this fragment
    assert result.underivable == [], (
        "unexpected underivable pairs (investigate before shipping): "
        + "; ".join(p.render() for p in result.underivable[:5])
    )
    # strongest internal consistency check (stage-3 review): with zero
    # collisions, every non-anchor term contributes exactly one pair
    assert result.fingerprint_collisions == 0
    assert len(result.verified) == result.n_terms - result.n_buckets
