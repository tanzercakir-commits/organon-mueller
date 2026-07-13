"""Composite-symmetry two-term decomposition (AO2016 Tables 3-4):
types 1-2, 1-3, 2-3 — three primary parameters (decision M31).

Same M28 discipline as `derive.py`: the equations are DERIVED by solving
rank-1 minors of the remainder H - alpha1*H1S sequentially (each minor
linear and conj-free in its unknown, structural guards enforced — K29);
the paper's Table 4 is only a comparison anchor in tests (K28).

Parameter conventions (scaled by alpha1 throughout):
* type 1-2 / 1-3: primaries x = alpha1*B (center), g = alpha1*G,
  h = alpha1*H; dependents A = g*conj(g)/x, C = h*conj(h)/x,
  M = g*conj(h)/x  (from AB=G*conj(G) [sic: AB=G G^*], GH^*=MB, BC=H H^*).
* type 2-3: primaries x = alpha1*A (corner), gs = alpha1*G^*,
  hs = alpha1*H^*; dependents B = gs*conj(gs)/x, C = hs*conj(hs)/x,
  Y = conj(hs)*gs/x  (from AB=GG^*, HG^*=AY, AC=HH^*).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import sympy as sp

from .covariance import mueller_from_standard_covariance
from .derive import generic_hermitian
from .solve import DecompositionError

__all__ = [
    "COMPOSITE_TYPES",
    "composite_template",
    "derive_composite",
    "decompose_composite",
    "CompositeDerived",
    "CompositeResult",
]

TYPE12, TYPE13, TYPE23 = "type1-2", "type1-3", "type2-3"
COMPOSITE_TYPES = (TYPE12, TYPE13, TYPE23)


def composite_template(symmetry: str, x, g, h) -> sp.Matrix:
    """Scaled alpha1*H1S templates (Table 3) from the three primaries."""
    cg, ch = sp.conjugate(g), sp.conjugate(h)
    if symmetry == TYPE12:
        a, c, m = g * cg / x, h * ch / x, g * ch / x
        return sp.Matrix([
            [a, g, g, m],
            [cg, x, x, ch],
            [cg, x, x, ch],
            [sp.conjugate(m), h, h, c],
        ])
    if symmetry == TYPE13:
        a, c, m = g * cg / x, h * ch / x, g * ch / x
        return sp.Matrix([
            [a, g, -g, m],
            [cg, x, -x, ch],
            [-cg, -x, x, -ch],
            [sp.conjugate(m), h, -h, c],
        ])
    if symmetry == TYPE23:
        # primaries here are gs = alpha1*G^*, hs = alpha1*H^* (row side,
        # conj-free minors live below the diagonal); template written in
        # terms of G = conj(gs), H = conj(hs)
        gg, hh = sp.conjugate(g), sp.conjugate(h)  # G, H
        b, c = g * sp.conjugate(g) / x, h * sp.conjugate(h) / x
        # entry (2,1) = alpha1*Y^* with Y = H G^*/A: since g = alpha1*G^*
        # and h = alpha1*H^*, Y^* = H^* G / A -> scaled: h * conj(g) / x
        y = h * gg / x
        return sp.Matrix([
            [x, gg, hh, x],
            [g, b, sp.conjugate(y), g],
            [h, y, c, h],
            [x, gg, hh, x],
        ])
    raise ValueError(f"unknown composite symmetry: {symmetry}")


#: sequential minor choices: (unknown_index, rows, cols); unknown order (x, g, h)
_MINORS = {
    TYPE12: (((1, 2), (1, 2)), ((0, 1), (1, 2)), ((3, 2), (1, 2))),
    TYPE13: (((1, 2), (1, 2)), ((0, 1), (1, 2)), ((3, 2), (1, 2))),
    TYPE23: (((0, 3), (0, 3)), ((1, 0), (0, 3)), ((2, 0), (0, 3))),
}

#: alpha1 = scaled trace: type 1-2/1-3: A + 2B + C; type 2-3: 2A + B + C
def _alpha_formula(symmetry: str, x, g, h) -> sp.Expr:
    if symmetry in (TYPE12, TYPE13):
        return g * sp.conjugate(g) / x + 2 * x + h * sp.conjugate(h) / x
    return 2 * x + g * sp.conjugate(g) / x + h * sp.conjugate(h) / x


@dataclass(frozen=True)
class CompositeDerived:
    symmetry: str
    x_expr: sp.Expr
    g_expr: sp.Expr
    h_expr: sp.Expr
    hermitian: sp.Matrix


def _minor(matrix: sp.Matrix, rows, cols) -> sp.Expr:
    return sp.expand(matrix.extract(list(rows), list(cols)).det())


@lru_cache(maxsize=None)
def derive_composite(symmetry: str) -> CompositeDerived:
    """Solve the three minors sequentially; structural guards per K29."""
    hmat = generic_hermitian()
    x = sp.symbols("x_c", real=True)
    g, h = sp.symbols("g_c h_c", complex=True)
    remainder = hmat - composite_template(symmetry, x, g, h)
    minors = _MINORS[symmetry]

    # x-minor: must not touch g/h entries
    eq_x = _minor(remainder, *minors[0])
    for probe in (g, h, sp.conjugate(g), sp.conjugate(h)):
        if eq_x.has(probe):
            raise ValueError(f"{symmetry}: x-minor touches {probe} (K29)")
    sols = sp.solve(eq_x, x)
    if len(sols) != 1:
        raise ValueError(f"{symmetry}: x-minor not uniquely solvable")
    x_expr = sp.simplify(sols[0])

    # g-minor: linear, conj(g)-free, h-free
    eq_g = _minor(remainder, *minors[1])
    for probe in (h, sp.conjugate(h), sp.conjugate(g)):
        if eq_g.has(probe):
            raise ValueError(f"{symmetry}: g-minor touches {probe} (K29)")
    sols = sp.solve(eq_g, g)
    if len(sols) != 1:
        raise ValueError(f"{symmetry}: g-minor not uniquely solvable")
    g_expr = sp.simplify(sols[0].subs(x, x_expr))

    # h-minor: linear, conj(h)-free, g-free
    eq_h = _minor(remainder, *minors[2])
    for probe in (g, sp.conjugate(g), sp.conjugate(h)):
        if eq_h.has(probe):
            raise ValueError(f"{symmetry}: h-minor touches {probe} (K29)")
    sols = sp.solve(eq_h, h)
    if len(sols) != 1:
        raise ValueError(f"{symmetry}: h-minor not uniquely solvable")
    h_expr = sp.simplify(sols[0].subs(x, x_expr))

    return CompositeDerived(symmetry, x_expr, g_expr, h_expr, hmat)


@dataclass
class CompositeResult:
    symmetry: str
    alpha1: float
    h1_scaled: np.ndarray
    h1: np.ndarray
    h2: np.ndarray
    m1: np.ndarray
    m2: np.ndarray


def _subs_map(hermitian: sp.Matrix, cov: np.ndarray) -> dict:
    mapping = {}
    for i in range(4):
        mapping[hermitian[i, i]] = complex(cov[i, i]).real
        for j in range(i + 1, 4):
            mapping[hermitian[i, j]] = complex(cov[i, j])
    return mapping


def decompose_composite(
    covariance: np.ndarray,
    symmetry: str,
    rank_tol: float = 1e-9,
    psd_tol: float = 1e-6,
    rank1_tol: float = 1e-6,
) -> CompositeResult:
    """Numeric composite-type decomposition with K26 guards."""
    cov = np.asarray(covariance, dtype=complex)
    if not np.all(np.isfinite(cov.real)) or not np.all(np.isfinite(cov.imag)):
        raise DecompositionError("covariance contains non-finite entries")
    cov = (cov + cov.conj().T) / 2

    # trace-1 convention guard (stage-9 review: a scaled covariance would
    # silently return a scaled alpha1 — K26 forbids wrong-but-plausible)
    trace = float(np.trace(cov).real)
    if abs(trace - 1.0) > 1e-6:
        raise DecompositionError(
            f"covariance trace is {trace:.6f}; normalize to m00 = 1 "
            "(trace-1 convention, AO2016)"
        )

    eig = np.linalg.eigvalsh(cov)
    lam_max = float(np.max(np.abs(eig)))
    rank = int(np.sum(np.abs(eig) > rank_tol * lam_max))
    if rank != 2:
        raise DecompositionError(
            f"covariance rank is {rank} (rank_tol={rank_tol}), need rank 2"
        )

    derived = derive_composite(symmetry)
    mapping = _subs_map(derived.hermitian, cov)

    values = {}
    for name, expr in (("x", derived.x_expr), ("g", derived.g_expr), ("h", derived.h_expr)):
        _, den = sp.fraction(sp.together(expr))
        if abs(complex(sp.N(den.subs(mapping)))) < 1e-8:
            raise DecompositionError(
                f"{symmetry}: {name}-denominator ~ 0 (missing-type anisotropy "
                "absent in the second component, or overlapping symmetry)"
            )
        values[name] = complex(sp.N(expr.subs(mapping)))

    x = values["x"]
    if abs(x.imag) > 1e-6 * (1 + abs(x)):
        raise DecompositionError(f"{symmetry}: primary not real ({x})")
    x = x.real
    if x <= 1e-9:
        raise DecompositionError(f"{symmetry}: primary <= 0 ({x})")

    xs = sp.symbols("xs", positive=True)
    gs, hs = sp.symbols("gs hs", complex=True)
    subs = {xs: x, gs: values["g"], hs: values["h"]}
    h1_scaled = np.array(
        sp.matrix2numpy(
            composite_template(symmetry, xs, gs, hs).subs(subs).evalf(),
            dtype=complex,
        )
    )
    alpha1 = complex(sp.N(_alpha_formula(symmetry, xs, gs, hs).subs(subs))).real
    if not (1e-9 < alpha1 < 1 - 1e-9):
        raise DecompositionError(f"{symmetry}: alpha1 out of (0,1): {alpha1}")

    h2 = (cov - h1_scaled) / (1 - alpha1)
    h2 = (h2 + h2.conj().T) / 2
    eig2 = np.linalg.eigvalsh(h2)
    if eig2.min() < -psd_tol:
        raise DecompositionError(f"{symmetry}: H2 not PSD (min eig {eig2.min():.2e})")
    if eig2[-2] > rank1_tol * max(eig2[-1], 1e-300):
        raise DecompositionError(
            f"{symmetry}: H2 not rank 1 (second eig {eig2[-2]:.2e})"
        )

    to_m = lambda hh: np.array(  # noqa: E731
        sp.matrix2numpy(
            mueller_from_standard_covariance(sp.Matrix(hh)).evalf(), dtype=complex
        )
    ).real
    return CompositeResult(
        symmetry=symmetry,
        alpha1=alpha1,
        h1_scaled=h1_scaled,
        h1=h1_scaled / alpha1,
        h2=h2,
        m1=to_m(h1_scaled / alpha1),
        m2=to_m(h2),
    )
