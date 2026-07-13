"""Stage-02 acceptance: the engine must REDISCOVER known structure (R1-R3),
must NOT invent commutativity (negative controls), and every harvested
candidate must survive independent numeric verification (100%).

Acceptance checks run on a size-9 saturation (the R3 terms have sizes 8 and
9); the full harvest pipeline runs at size 7 to keep CI economical.
"""
import pytest

egglog = pytest.importorskip("egglog")  # decision M13: optional extra

from organon_mueller.discovery.engine import DiscoveryEngine  # noqa: E402
from organon_mueller.discovery.interpret import terms_numerically_equal  # noqa: E402
from organon_mueller.discovery.terms import (  # noqa: E402
    Atom,
    Conj,
    Mul,
    enumerate_terms,
)

A, B = Atom("a"), Atom("b")
R2_LHS, R2_RHS = Mul(A, Conj(B)), Mul(Conj(B), A)
R3_LHS = Mul(Mul(A, B), Conj(Mul(A, B)))
R3_RHS = Mul(Mul(A, Conj(A)), Mul(B, Conj(B)))


@pytest.fixture(scope="module")
def engine9() -> DiscoveryEngine:
    return DiscoveryEngine(atom_names=("a", "b"), max_size=9)


@pytest.fixture(scope="module")
def saturated9(engine9):
    egraph, _ = engine9.saturate(enumerate_terms(("a", "b"), 9))
    return egraph


def test_enumeration_deterministic_and_sized():
    terms = enumerate_terms(("a", "b"), 7)
    assert terms == enumerate_terms(("a", "b"), 7)  # K12
    assert all(t.size() <= 7 for t in terms)
    assert len(terms) == len(set(terms))  # hashable, no duplicates
    assert R3_LHS.size() == 8 and R3_RHS.size() == 9  # documented correction


def test_r1_conj_involution(engine9, saturated9):
    assert engine9.equivalent(saturated9, Conj(Conj(A)), A)


def test_r2_atom_commutation(engine9, saturated9):
    assert engine9.equivalent(saturated9, R2_LHS, R2_RHS)


def test_r3_serial_mueller_product(engine9, saturated9):
    """(a*b)*conj(a*b) == (a*conj(a)) * (b*conj(b))  — I10 consequence."""
    assert engine9.equivalent(saturated9, R3_LHS, R3_RHS)
    # and it is TRUE numerically, independent of the e-graph:
    assert terms_numerically_equal(R3_LHS, R3_RHS, ("a", "b"))


def test_negative_control_no_plain_commutativity(engine9, saturated9):
    assert not engine9.equivalent(saturated9, Mul(A, B), Mul(B, A))
    assert not terms_numerically_equal(Mul(A, B), Mul(B, A), ("a", "b"))


def test_negative_control_no_conj_conj_commutativity(engine9, saturated9):
    lhs, rhs = Mul(Conj(A), Conj(B)), Mul(Conj(B), Conj(A))
    assert not engine9.equivalent(saturated9, lhs, rhs)
    # indeed FALSE numerically, so the e-graph is right to keep them apart
    assert not terms_numerically_equal(lhs, rhs, ("a", "b"))


def test_full_run_all_candidates_verified():
    result = DiscoveryEngine(atom_names=("a", "b"), max_size=7).run()
    assert result.n_terms > 500  # size-7 enumeration over two atoms
    assert result.verified, "engine harvested no equivalences at all"
    assert result.sound, (
        "unsound axiom signal — refuted candidates: "
        + "; ".join(p.render() for p in result.refuted[:5])
    )
    assert result.extraction_collisions == 0  # completeness guard
    # the I10 commutation pair must be rediscovered in the harvest
    harvested = {frozenset((p.left, p.right)) for p in result.verified}
    assert frozenset((R2_LHS, R2_RHS)) in harvested
