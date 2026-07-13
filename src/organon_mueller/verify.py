"""Verification helpers: exact symbolic checks and random numeric sampling.

Stage-00 decision M2: every identity is verified symbolically when
tractable, otherwise numerically over random complex samples with a fixed
seed (K2: CI must be deterministic).
"""
from __future__ import annotations

from typing import Callable

import numpy as np
import sympy as sp

from .algebra.states import HVector

__all__ = [
    "symbolic_zero",
    "symbolic_equal",
    "to_numpy",
    "random_params",
    "random_hvector",
    "random_stokes",
    "numeric_equal",
    "sample_check",
]

DEFAULT_SEED = 20260713
DEFAULT_SAMPLES = 50
ATOL = 1e-9


# -- symbolic ---------------------------------------------------------------

def symbolic_zero(expr: sp.Expr) -> bool:
    """Exact zero test for polynomial expressions (expand-based)."""
    return sp.expand(expr) == 0


def symbolic_equal(a: sp.Matrix, b: sp.Matrix) -> bool:
    """Entrywise exact equality of two symbolic matrices."""
    diff = sp.expand(a - b)
    return all(e == 0 for e in diff)


# -- numeric ----------------------------------------------------------------

def to_numpy(m: sp.Matrix) -> np.ndarray:
    """Evaluate a (numeric) SymPy matrix to a complex NumPy array."""
    return np.array(sp.matrix2numpy(sp.Matrix(m).evalf(), dtype=complex))


def random_params(rng: np.random.Generator, n: int = 4) -> list[complex]:
    """Standard-normal complex parameters."""
    return [
        complex(x, y)
        for x, y in zip(rng.standard_normal(n), rng.standard_normal(n))
    ]


def random_hvector(rng: np.random.Generator) -> HVector:
    t, a, b, g = (sp.sympify(p) for p in random_params(rng))
    return HVector(t, a, b, g)


def random_stokes(rng: np.random.Generator) -> list[float]:
    """Random real Stokes 4-vector (not necessarily physical; algebra only)."""
    return [float(x) for x in rng.standard_normal(4)]


def numeric_equal(a, b, atol: float = ATOL) -> bool:
    an, bn = np.asarray(a, dtype=complex), np.asarray(b, dtype=complex)
    scale = max(float(np.max(np.abs(an))), float(np.max(np.abs(bn))), 1.0)
    return bool(np.allclose(an, bn, atol=atol * scale, rtol=0))


def sample_check(
    check: Callable[[np.random.Generator], bool],
    samples: int = DEFAULT_SAMPLES,
    seed: int = DEFAULT_SEED,
) -> bool:
    """Run a randomized check `samples` times with a deterministic seed."""
    rng = np.random.default_rng(seed)
    return all(check(rng) for _ in range(samples))
