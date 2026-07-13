"""Numeric interpretation of abstract terms — the SymPy/NumPy half of the
hybrid engine (decision M10).

An assignment maps each atom name to a concrete Z matrix (from a random
nondepolarizing state).  Mul is matrix multiplication, Conj the elementwise
conjugate.  Two terms are accepted as numerically equal when they agree on
several independent random assignments.
"""
from __future__ import annotations

import numpy as np

from ..verify import numeric_equal, random_hvector, to_numpy
from .terms import Atom, Conj, Mul, Term

__all__ = ["random_assignment", "evaluate", "terms_numerically_equal"]


def random_assignment(
    atom_names: tuple[str, ...], rng: np.random.Generator
) -> dict[str, np.ndarray]:
    """Independent random Z matrices for every atom."""
    return {name: to_numpy(random_hvector(rng).to_z()) for name in atom_names}


def evaluate(term: Term, assignment: dict[str, np.ndarray]) -> np.ndarray:
    if isinstance(term, Atom):
        return assignment[term.name]
    if isinstance(term, Mul):
        return evaluate(term.left, assignment) @ evaluate(term.right, assignment)
    if isinstance(term, Conj):
        return np.conj(evaluate(term.arg, assignment))
    raise TypeError(f"unknown term node: {term!r}")


def terms_numerically_equal(
    a: Term,
    b: Term,
    atom_names: tuple[str, ...],
    draws: int = 3,
    seed: int = 20260713,
) -> bool:
    """Equality on `draws` independent random assignments (deterministic seed)."""
    rng = np.random.default_rng(seed)
    for _ in range(draws):
        assignment = random_assignment(atom_names, rng)
        if not numeric_equal(evaluate(a, assignment), evaluate(b, assignment)):
            return False
    return True
