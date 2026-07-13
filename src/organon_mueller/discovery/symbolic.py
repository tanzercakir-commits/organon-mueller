"""Symbolic-EXACT evaluation of abstract terms (VERIFICATION.md layer 1
wired into discovery, stage 4, decision M19).

Each atom is assigned the Z matrix of a fresh generic complex state
(tau_i, alpha_i, beta_i, gamma_i) — one INDEPENDENT parameter set per atom
(rule K17; sharing parameters would prove false "identities").  Mul is
matrix multiplication, Conj the elementwise conjugate.  Equality is decided
by `expand`-based exact zero testing of every entry: for these polynomial
expressions this is a PROOF, not a sample.
"""
from __future__ import annotations

import sympy as sp

from ..algebra.states import HVector
from ..verify import symbolic_equal
from .terms import Atom, Conj, Mul, Term

__all__ = [
    "symbolic_assignment",
    "evaluate_symbolic",
    "terms_symbolically_equal",
]


def symbolic_assignment(atom_names: tuple[str, ...]) -> dict[str, sp.Matrix]:
    """Fresh generic symbolic Z matrix per atom (independent parameters, K17)."""
    return {name: HVector.generic(name).to_z() for name in atom_names}


def evaluate_symbolic(term: Term, assignment: dict[str, sp.Matrix]) -> sp.Matrix:
    if isinstance(term, Atom):
        return assignment[term.name]
    if isinstance(term, Mul):
        return sp.expand(
            evaluate_symbolic(term.left, assignment)
            * evaluate_symbolic(term.right, assignment)
        )
    if isinstance(term, Conj):
        return evaluate_symbolic(term.arg, assignment).conjugate()
    raise TypeError(f"unknown term node: {term!r}")


def terms_symbolically_equal(
    a: Term, b: Term, atom_names: tuple[str, ...]
) -> bool:
    """EXACT equality proof of two terms over generic states."""
    assignment = symbolic_assignment(atom_names)
    return symbolic_equal(
        evaluate_symbolic(a, assignment), evaluate_symbolic(b, assignment)
    )
