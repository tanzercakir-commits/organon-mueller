"""Numeric two-term decomposition solver (AO2016 automation, stage 8).

Given a depolarizing Mueller matrix (or its standard-basis covariance)
whose rank-2 covariance is the convex mix of a SYMMETRIC pure component
(type 1/2/3) and an arbitrary pure component, recover alpha1, H1S, H2
and the component Mueller matrices — using the equations DERIVED by
`derive.py` (decision M28), never hand-copied ones.

Guards (rule K26 / user directive): every inapplicable or unphysical
configuration raises `DecompositionError` with a reason; silent NaNs or
wrong-but-plausible outputs are design bugs.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import sympy as sp

from .covariance import (
    SYMMETRY_TEMPLATES,
    mueller_from_standard_covariance,
    standard_covariance_from_mueller,
)
from .derive import MINOR_CHOICES, DerivedEquations, derive_equations

__all__ = ["DecompositionError", "DecompositionResult", "decompose"]

_TOL = 1e-9
_DENOM_TOL = 1e-8


class DecompositionError(ValueError):
    """The two-term symmetric decomposition is not applicable here."""


@dataclass
class DecompositionResult:
    symmetry: str
    variant: str
    alpha1: float
    h1_scaled: np.ndarray   # alpha1 * H1S
    h1: np.ndarray          # H1S (trace 1)
    h2: np.ndarray          # H2 (trace 1)
    m1: np.ndarray
    m2: np.ndarray


@lru_cache(maxsize=None)
def _derived(symmetry: str, variant: str) -> DerivedEquations:
    return derive_equations(symmetry, variant)


@lru_cache(maxsize=None)
def _denominators(symmetry: str, variant: str):
    eq = _derived(symmetry, variant)
    dens = []
    for expr in (eq.x_expr, eq.w_expr):
        _, den = sp.fraction(sp.together(expr))
        dens.append(den)
    return tuple(dens)


def _subs_map(eq: DerivedEquations, cov: np.ndarray) -> dict:
    mapping = {}
    for i in range(4):
        mapping[eq.hermitian[i, i]] = complex(cov[i, i]).real
        for j in range(i + 1, 4):
            mapping[eq.hermitian[i, j]] = complex(cov[i, j])
    return mapping


def _evaluate(expr: sp.Expr, mapping: dict) -> complex:
    return complex(sp.N(expr.subs(mapping)))


def _hermitize(cov: np.ndarray) -> np.ndarray:
    return (cov + cov.conj().T) / 2


def _try_variant(
    symmetry: str,
    variant: str,
    cov: np.ndarray,
    psd_tol: float = 1e-6,
    rank1_tol: float = 1e-6,
) -> DecompositionResult:
    eq = _derived(symmetry, variant)
    mapping = _subs_map(eq, cov)

    for den in _denominators(symmetry, variant):
        if abs(_evaluate(den, mapping)) < _DENOM_TOL:
            raise DecompositionError(
                f"{symmetry}/{variant}: determinant denominator ~ 0 "
                "(overlapping symmetries or inapplicable variant)"
            )

    x = _evaluate(eq.x_expr, mapping)
    if abs(x.imag) > 1e-6 * (1 + abs(x)):
        raise DecompositionError(f"{symmetry}/{variant}: primary parameter not real ({x})")
    x = x.real
    if x <= _TOL:
        raise DecompositionError(f"{symmetry}/{variant}: primary parameter <= 0 ({x})")
    w = _evaluate(eq.w_expr, mapping)

    template, alpha_formula = SYMMETRY_TEMPLATES[symmetry]
    xs, ws = sp.symbols("xs", positive=True), sp.symbols("ws", complex=True)
    h1_scaled_sym = template(xs, ws, primary=eq.primary)
    subs = {xs: x, ws: w}
    h1_scaled = np.array(
        sp.matrix2numpy(h1_scaled_sym.subs(subs).evalf(), dtype=complex)
    )
    alpha1 = complex(sp.N(alpha_formula(xs, ws).subs(subs))).real

    if not (_TOL < alpha1 < 1 - _TOL):
        raise DecompositionError(f"{symmetry}/{variant}: alpha1 out of (0,1): {alpha1}")

    h2_scaled = cov - h1_scaled
    alpha2 = 1 - alpha1
    h1 = h1_scaled / alpha1
    h2 = _hermitize(h2_scaled / alpha2)

    # physicality guards: H2 must be PSD and rank 1 (within tolerance;
    # tolerances are parameters because printed/experimental data carries
    # rounding noise — e.g. 4-decimal literature values need ~1e-3)
    eig = np.linalg.eigvalsh(h2)
    if eig.min() < -psd_tol:
        raise DecompositionError(
            f"{symmetry}/{variant}: recovered H2 not PSD (min eig {eig.min():.2e})"
        )
    if eig[-2] > rank1_tol * max(eig[-1], 1e-300):
        raise DecompositionError(
            f"{symmetry}/{variant}: recovered H2 not rank 1 "
            f"(second eigenvalue {eig[-2]:.2e})"
        )

    return DecompositionResult(
        symmetry=symmetry,
        variant=variant,
        alpha1=alpha1,
        h1_scaled=h1_scaled,
        h1=h1,
        h2=h2,
        m1=np.array(
            sp.matrix2numpy(
                mueller_from_standard_covariance(sp.Matrix(h1)).evalf(), dtype=complex
            )
        ).real,
        m2=np.array(
            sp.matrix2numpy(
                mueller_from_standard_covariance(sp.Matrix(h2)).evalf(), dtype=complex
            )
        ).real,
    )


def decompose(
    mueller: np.ndarray | None = None,
    covariance: np.ndarray | None = None,
    symmetry: str = "type1",
    variant: str = "auto",
    rank_tol: float = 1e-9,
    psd_tol: float = 1e-6,
    rank1_tol: float = 1e-6,
) -> DecompositionResult:
    """Two-term decomposition with H1 of the given symmetry type.

    Provide either the (m00-normalized) Mueller matrix or its
    standard-basis covariance. `variant="auto"` orders the paper's a/b
    equation sets by guard-denominator magnitude (the paper's numerical
    advice) and returns the first that passes all guards. Tolerances:
    exact synthetic data works with the strict defaults; rounded
    literature/experimental data needs looser values (e.g. 1e-4/1e-3
    for 4-decimal prints).
    """
    if (mueller is None) == (covariance is None):
        raise ValueError("provide exactly one of mueller / covariance")
    if covariance is None:
        m = sp.Matrix(np.asarray(mueller, dtype=float))
        covariance = np.array(
            sp.matrix2numpy(standard_covariance_from_mueller(m).evalf(), dtype=complex)
        )
    cov = _hermitize(np.asarray(covariance, dtype=complex))

    # rank-2 guard
    eig = np.linalg.eigvalsh(cov)
    lam_max = float(np.max(np.abs(eig)))
    rank = int(np.sum(np.abs(eig) > rank_tol * lam_max))
    if rank != 2:
        raise DecompositionError(
            f"covariance rank is {rank} (rank_tol={rank_tol}), "
            "two-term decomposition needs rank 2"
        )

    if variant == "auto":
        # paper's advice (AO2016 Sec. 4): prefer the variant whose guard
        # determinant/denominator has the larger magnitude (numerically
        # healthier) — implemented post stage-8 review
        def _health(v: str) -> float:
            eq = _derived(symmetry, v)
            mapping = _subs_map(eq, cov)
            return min(
                abs(_evaluate(den, mapping))
                for den in _denominators(symmetry, v)
            )

        variants = tuple(sorted(("a", "b"), key=_health, reverse=True))
    else:
        variants = (variant,)
    errors = []
    for v in variants:
        if (symmetry, v) not in MINOR_CHOICES:
            raise ValueError(f"unknown symmetry/variant: {symmetry}/{v}")
        try:
            return _try_variant(
                symmetry, v, cov, psd_tol=psd_tol, rank1_tol=rank1_tol
            )
        except DecompositionError as exc:
            errors.append(str(exc))
    raise DecompositionError("; ".join(errors))
