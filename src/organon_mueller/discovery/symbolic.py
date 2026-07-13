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
from .terms import Atom, Conj, Mul, Scalar, ScalarAtom, ScalarConj, Scale, Sum, Term

__all__ = [
    "symbolic_assignment",
    "evaluate_symbolic",
    "evaluate_scalar_symbolic",
    "terms_symbolically_equal",
]


def symbolic_assignment(
    atom_names: tuple[str, ...], scalar_names: tuple[str, ...] = ()
) -> dict:
    """Fresh generic symbolic Z matrix per atom and a fresh independent
    complex symbol per scalar (independence rule K17 extends to scalars)."""
    assignment: dict = {name: HVector.generic(name).to_z() for name in atom_names}
    for name in scalar_names:
        assignment[name] = sp.symbols(f"scl_{name}", complex=True)
    return assignment


def evaluate_scalar_symbolic(scalar: Scalar, assignment) -> sp.Expr:
    if isinstance(scalar, ScalarAtom):
        return assignment[scalar.name]
    if isinstance(scalar, ScalarConj):
        return sp.conjugate(evaluate_scalar_symbolic(scalar.arg, assignment))
    raise TypeError(f"unknown scalar node: {scalar!r}")


def evaluate_symbolic(term: Term, assignment) -> sp.Matrix:
    if isinstance(term, Atom):
        return assignment[term.name]
    if isinstance(term, Mul):
        return sp.expand(
            evaluate_symbolic(term.left, assignment)
            * evaluate_symbolic(term.right, assignment)
        )
    if isinstance(term, Conj):
        return evaluate_symbolic(term.arg, assignment).conjugate()
    if isinstance(term, Sum):
        return sp.expand(
            evaluate_symbolic(term.left, assignment)
            + evaluate_symbolic(term.right, assignment)
        )
    if isinstance(term, Scale):
        return sp.expand(
            evaluate_scalar_symbolic(term.coeff, assignment)
            * evaluate_symbolic(term.arg, assignment)
        )
    raise TypeError(f"unknown term node: {term!r}")


def terms_symbolically_equal(
    a: Term, b: Term, atom_names: tuple[str, ...],
    scalar_names: tuple[str, ...] = (),
) -> bool:
    """EXACT equality proof of two terms over generic states and scalars."""
    assignment = symbolic_assignment(atom_names, scalar_names)
    return symbolic_equal(
        evaluate_symbolic(a, assignment), evaluate_symbolic(b, assignment)
    )
