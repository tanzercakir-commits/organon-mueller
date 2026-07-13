"""Stage-4: the symbolic-EXACT layer wired into discovery (M19)."""
import pytest
import sympy as sp

from organon_mueller.discovery.symbolic import (
    evaluate_symbolic,
    symbolic_assignment,
    terms_symbolically_equal,
)
from organon_mueller.discovery.terms import Atom, Conj, Mul

A, B = Atom("a"), Atom("b")
R3_LHS = Mul(Mul(A, B), Conj(Mul(A, B)))
R3_RHS = Mul(Mul(A, Conj(A)), Mul(B, Conj(B)))


def test_assignment_uses_independent_parameters():
    """K17: shared parameters would prove false identities."""
    assignment = symbolic_assignment(("a", "b"))
    syms_a = assignment["a"].free_symbols
    syms_b = assignment["b"].free_symbols
    assert syms_a and syms_b and not (syms_a & syms_b)


def test_r2_commutation_exact():
    assert terms_symbolically_equal(Mul(A, Conj(B)), Mul(Conj(B), A), ("a", "b"))


def test_r3_serial_mueller_exact():
    """Layer-1 proof of the serial Mueller product law (not a sample)."""
    assert terms_symbolically_equal(R3_LHS, R3_RHS, ("a", "b"))


def test_negative_exact():
    assert not terms_symbolically_equal(Mul(A, B), Mul(B, A), ("a", "b"))
    assert not terms_symbolically_equal(
        Mul(Conj(A), Conj(B)), Mul(Conj(B), Conj(A)), ("a", "b")
    )


def test_conj_is_elementwise_not_dagger():
    """conj(a*b) == conj(a)*conj(b), and is NOT the conjugate transpose."""
    assert terms_symbolically_equal(
        Conj(Mul(A, B)), Mul(Conj(A), Conj(B)), ("a", "b")
    )
    assignment = symbolic_assignment(("a",))
    z = assignment["a"]
    assert sp.expand(evaluate_symbolic(Conj(A), assignment) - z.conjugate()) == sp.zeros(4, 4)
    dagger_diff = sp.expand(evaluate_symbolic(Conj(A), assignment) - z.H)
    assert any(e != 0 for e in dagger_diff)


def test_mueller_reality_via_terms():
    """a*conj(a) evaluates to a real matrix (M = ZZ*), exactly."""
    assignment = symbolic_assignment(("a",))
    m = evaluate_symbolic(Mul(A, Conj(A)), assignment)
    assert all(sp.expand(e - sp.conjugate(e)) == 0 for e in m)
