"""THE DERIVER (decision M28): produce the two-term decomposition
equations from rank-1 minor conditions — do not copy the paper's table.

For a symmetry type with scaled parameters (x, w), the remainder
R = H - alpha1*H1S must be rank 1, so every 2x2 minor of R vanishes.
Following AO2016 Section 4, a chosen pair of minors determines x and w
sequentially (each equation is LINEAR in its unknown). The derived
closed forms are then compared SYMBOLICALLY against the hand-entered
Table 2 anchors in tests (rule K28: exact zero difference required).
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .covariance import SYMMETRY_TEMPLATES, TYPE1, TYPE2, TYPE3

__all__ = ["DerivedEquations", "derive_equations", "generic_hermitian", "MINOR_CHOICES"]


def generic_hermitian() -> sp.Matrix:
    """Generic 4x4 Hermitian H: h_ij free complex above the diagonal,
    real on the diagonal, h_ji = conj(h_ij)."""
    entries = {}
    for i in range(4):
        entries[(i, i)] = sp.symbols(f"h{i}{i}", real=True)
        for j in range(i + 1, 4):
            entries[(i, j)] = sp.symbols(f"h{i}{j}", complex=True)
            entries[(j, i)] = sp.conjugate(entries[(i, j)])
    return sp.Matrix(4, 4, lambda i, j: entries[(i, j)])


#: per type/variant: primary parameter position, then the two minors (as
#: (rows, cols) index pairs on the remainder) that determine x then w —
#: chosen as in AO2016 Section 4 (variant a = outer/DetA-side minors,
#: variant b = central/DetB-side minors). The w-minors are chosen on the
#: upper (non-conjugated) side so they are conj-free and linear in w;
#: the paper's 3a solves V* on the conjugate side — equivalent by
#: conjugation (tests anchor against the conjugated paper formula).
MINOR_CHOICES = {
    (TYPE1, "a"): ("outer", ((0, 1), (0, 1)), ((0, 1), (0, 3))),
    (TYPE1, "b"): ("outer", ((0, 2), (0, 2)), ((0, 2), (0, 3))),
    (TYPE2, "a"): ("outer", ((0, 3), (0, 3)), ((0, 3), (0, 1))),
    (TYPE2, "b"): ("center", ((1, 2), (1, 2)), ((0, 1), (1, 2))),
    (TYPE3, "a"): ("outer", ((0, 3), (0, 3)), ((0, 3), (0, 1))),
    (TYPE3, "b"): ("center", ((1, 2), (1, 2)), ((0, 1), (1, 2))),
}


@dataclass(frozen=True)
class DerivedEquations:
    symmetry: str
    variant: str
    primary: str  # "outer" (P/K/E) or "center" (Pbar/Kbar/Ebar)
    x_expr: sp.Expr  # alpha1 * primary parameter, in terms of h_ij
    w_expr: sp.Expr  # alpha1 * (W|N|V) in terms of h_ij
    hermitian: sp.Matrix  # the generic H the expressions refer to


def _minor(matrix: sp.Matrix, rows, cols) -> sp.Expr:
    sub = matrix.extract(list(rows), list(cols))
    return sp.expand(sub.det())


def derive_equations(symmetry: str, variant: str = "a") -> DerivedEquations:
    """Derive (x, w) closed forms for the given symmetry type and variant.

    Strategy (AO2016 Section 4, automated): the x-minor touches only
    template entries carrying the primary parameter, so after the rank-1
    quadratics cancel it is LINEAR in x; the w-minor is chosen on the
    non-conjugated side, linear in w. Any deviation (multiple roots,
    conj(w) appearing) raises instead of guessing.
    """
    template, _ = SYMMETRY_TEMPLATES[symmetry]
    primary, (rows_x, cols_x), (rows_w, cols_w) = MINOR_CHOICES[(symmetry, variant)]
    hmat = generic_hermitian()

    # Equation 1: solve the x-minor. Build the remainder with a PLAIN x
    # placeholder in the primary slots only — the dependent slots carry
    # w*conj(w)/x which the chosen x-minor never touches; enforce that
    # structurally by checking the minor is a polynomial in x alone.
    x = sp.symbols("x_p", real=True)
    w_probe = sp.symbols("w_probe", complex=True)
    remainder = hmat - template(x, w_probe, primary=primary)
    eq_x = _minor(remainder, rows_x, cols_x)
    if eq_x.has(w_probe) or eq_x.has(sp.conjugate(w_probe)):
        raise ValueError(f"{symmetry}/{variant}: x-minor touches w entries")
    sol_x = sp.solve(eq_x, x)
    if len(sol_x) != 1:
        raise ValueError(
            f"{symmetry}/{variant}: x-minor not uniquely solvable ({len(sol_x)} roots)"
        )
    x_expr = sp.simplify(sol_x[0])

    # Equation 2: solve the w-minor (conj-free by minor choice).
    w_sym = sp.symbols("w_full", complex=True)
    remainder_w = hmat - template(x, w_sym, primary=primary)
    eq_w = _minor(remainder_w, rows_w, cols_w)
    if eq_w.has(sp.conjugate(w_sym)):
        raise ValueError(f"{symmetry}/{variant}: w-minor involves conj(w)")
    sol_w = sp.solve(eq_w, w_sym)
    if len(sol_w) != 1:
        raise ValueError(
            f"{symmetry}/{variant}: w-minor not uniquely solvable ({len(sol_w)} roots)"
        )
    w_expr = sp.simplify(sol_w[0].subs(x, x_expr))

    return DerivedEquations(
        symmetry=symmetry, variant=variant, primary=primary,
        x_expr=x_expr, w_expr=w_expr, hermitian=hmat,
    )
