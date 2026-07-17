"""Lorentz face of the Z-matrix algebra (milestone L0, FROZEN-7).

Source: the collaborator's written work order (2026-07-17) defining the
Σ^μ basis (4×4 generalization of the Pauli σ^μ), Z = α_μΣ^μ with complex
α, Σ̄^μ = (Σ⁰, −Σ¹, −Σ², −Σ³), and Λ = ZZ* as "the most general form of
the Lorentz matrix".

The pre-implementation probe established (and the tests lock
symbolically):

- Σ^μ is EXACTLY this engine's existing Z-matrix basis (the polarization
  Z of the papers) — the Mueller↔Lorentz bridge is a theorem here, not
  an analogy: M = ZZ* and Λ = ZZ* are the same formula on the two faces.
- Guard-free theorem: Z(α)·Z̄(α) = (α·α)·I with
  α·α ≡ α₀² − α₁² − α₂² − α₃² (Minkowski square). The spec's inverse
  formula Z⁻¹ = α_μΣ̄^μ is its α·α = 1 corollary — a genuine
  Horn-conditional identity (guard: unit Minkowski square).
- Λ^T g Λ = (α·α)(α·α)* g for GENERIC complex α; under the guard this is
  the Lorentz property.

CONVENTION NOTES (M29-style; the spec itself warns that sign differences
are conventions, not errors):
- boosts:    α = (cosh(φ/2), sinh(φ/2)·n̂)   — real spatial part;
  x-boost reproduces the textbook matrix [[coshφ, sinhφ, 0, 0], ...].
- rotations: α = (cos(θ/2), i·sin(θ/2)·n̂)  — imaginary spatial part;
  a z-rotation lands in Λ with R[1][2] = +sin θ, R[2][1] = −sin θ.
"""
from __future__ import annotations

import sympy as sp

__all__ = [
    "SIGMA", "SIGMA_BAR", "METRIC",
    "z_matrix", "z_bar_matrix", "minkowski_square", "z_inverse",
    "lorentz_matrix", "boost_alpha", "rotation_alpha",
]

# Authoritative literals, transcribed from the work order. Their equality
# with the engine's HVector Z-basis is locked by a TEST (the bridge), not
# assumed here.
SIGMA = (
    sp.eye(4),
    sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
               [0, 0, 0, -sp.I], [0, 0, sp.I, 0]]),
    sp.Matrix([[0, 0, 1, 0], [0, 0, 0, sp.I],
               [1, 0, 0, 0], [0, -sp.I, 0, 0]]),
    sp.Matrix([[0, 0, 0, 1], [0, 0, -sp.I, 0],
               [0, sp.I, 0, 0], [1, 0, 0, 0]]),
)

SIGMA_BAR = (SIGMA[0], -SIGMA[1], -SIGMA[2], -SIGMA[3])

#: Minkowski metric, signature (+, -, -, -)
METRIC = sp.diag(1, -1, -1, -1)


def _as_four(alpha):
    alpha = tuple(sp.sympify(a) for a in alpha)
    if len(alpha) != 4:
        raise ValueError("alpha must have exactly 4 components")
    return alpha


def z_matrix(alpha) -> sp.Matrix:
    """Z(α) = α_μ Σ^μ (complex α allowed)."""
    alpha = _as_four(alpha)
    return sp.expand(sum((alpha[m] * SIGMA[m] for m in range(4)),
                         sp.zeros(4)))


def z_bar_matrix(alpha) -> sp.Matrix:
    """Z̄(α) = α_μ Σ̄^μ."""
    alpha = _as_four(alpha)
    return sp.expand(sum((alpha[m] * SIGMA_BAR[m] for m in range(4)),
                         sp.zeros(4)))


def minkowski_square(alpha):
    """α·α = α₀² − α₁² − α₂² − α₃² (the guard quantity)."""
    a = _as_four(alpha)
    return sp.expand(a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2)


def z_inverse(alpha) -> sp.Matrix:
    """Z(α)⁻¹ = Z̄(α)/(α·α), valid on the guard α·α ≠ 0 (the spec's
    Z⁻¹ = α_μΣ̄^μ is the α·α = 1 case). Raises if α·α is identically
    zero; for symbolic α the nonvanishing of α·α is the caller's guard
    (K26: reasons, not silent wrongness)."""
    alpha = _as_four(alpha)
    q = minkowski_square(alpha)
    if q == 0:
        raise ValueError("alpha has identically zero Minkowski square "
                         "(alpha.alpha = 0): Z is not invertible by the "
                         "Sigma-bar formula on this locus")
    return sp.expand(z_bar_matrix(alpha) / q)


def lorentz_matrix(alpha) -> sp.Matrix:
    """Λ(α) = Z(α)·Z(α)* (elementwise complex conjugate, NO transpose —
    the engine's M = ZZ* on the polarization face, verbatim)."""
    z = z_matrix(alpha)
    return sp.expand(z * z.conjugate())


def boost_alpha(phi, n=(1, 0, 0)):
    """Boost parameters α = (cosh(φ/2), sinh(φ/2)·n̂); n̂ must be a unit
    3-vector (symbolically checked when decidable)."""
    n = tuple(sp.sympify(c) for c in n)
    if len(n) != 3:
        raise ValueError("n must have 3 components")
    norm2 = sp.simplify(n[0]**2 + n[1]**2 + n[2]**2)
    if norm2 not in (1, sp.Integer(1)) and sp.simplify(norm2 - 1) != 0:
        raise ValueError(f"n must be a unit vector (|n|^2 = {norm2})")
    phi = sp.sympify(phi)
    ch, sh = sp.cosh(phi / 2), sp.sinh(phi / 2)
    return (ch, sh * n[0], sh * n[1], sh * n[2])


def rotation_alpha(theta, n=(0, 0, 1)):
    """Rotation parameters α = (cos(θ/2), i·sin(θ/2)·n̂) — imaginary
    spatial part (convention note in the module docstring)."""
    n = tuple(sp.sympify(c) for c in n)
    if len(n) != 3:
        raise ValueError("n must have 3 components")
    norm2 = sp.simplify(n[0]**2 + n[1]**2 + n[2]**2)
    if norm2 not in (1, sp.Integer(1)) and sp.simplify(norm2 - 1) != 0:
        raise ValueError(f"n must be a unit vector (|n|^2 = {norm2})")
    theta = sp.sympify(theta)
    c, s = sp.cos(theta / 2), sp.sin(theta / 2)
    return (c, sp.I * s * n[0], sp.I * s * n[1], sp.I * s * n[2])
