"""Biquaternions (quaternions with complex components).

A medium state is the biquaternion  h = tau*1 + (i*alpha)*i + (i*beta)*j
+ (i*gamma)*k  (arXiv:1705.07147, Eq. (17)).  We store the four Hamilton
components (w, x, y, z) with respect to the basis (1, i, j, k); for a
medium state these are (tau, I*alpha, I*beta, I*gamma).

Two conjugations coexist and must not be confused (stage-00 warning 2):

* Hamilton conjugate  bar(q)  = (w, -x, -y, -z)
* Hermitian conjugate q^dagger = componentwise complex conjugate of bar(q),
  i.e. (w*, -x*, -y*, -z*).  For a medium state this reproduces the paper's
  h^dagger = tau^* 1 + i alpha^* i + i beta^* j + i gamma^* k.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .basis import Q_I, Q_J, Q_K, Q_ONE

__all__ = ["BiQuaternion"]


@dataclass(frozen=True)
class BiQuaternion:
    """Quaternion w + x*i + y*j + z*k with complex (SymPy) components."""

    w: sp.Expr
    x: sp.Expr
    y: sp.Expr
    z: sp.Expr

    def __post_init__(self) -> None:
        for name in ("w", "x", "y", "z"):
            object.__setattr__(self, name, sp.sympify(getattr(self, name)))

    # -- algebra ---------------------------------------------------------
    def __mul__(self, other: "BiQuaternion") -> "BiQuaternion":
        """Hamilton product (i^2 = j^2 = k^2 = ijk = -1)."""
        if not isinstance(other, BiQuaternion):
            return NotImplemented
        a, b = self, other
        return BiQuaternion(
            w=a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
            x=a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
            y=a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
            z=a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w,
        )

    def __add__(self, other: "BiQuaternion") -> "BiQuaternion":
        return BiQuaternion(
            self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z
        )

    def scale(self, c: sp.Expr) -> "BiQuaternion":
        return BiQuaternion(c * self.w, c * self.x, c * self.y, c * self.z)

    # -- conjugations ----------------------------------------------------
    def hamilton_conjugate(self) -> "BiQuaternion":
        """bar(q): flip the sign of the vector part."""
        return BiQuaternion(self.w, -self.x, -self.y, -self.z)

    def hermitian_conjugate(self) -> "BiQuaternion":
        """q^dagger: complex-conjugate the components of bar(q)."""
        return BiQuaternion(
            sp.conjugate(self.w),
            -sp.conjugate(self.x),
            -sp.conjugate(self.y),
            -sp.conjugate(self.z),
        )

    # -- representations --------------------------------------------------
    def to_matrix(self) -> sp.Matrix:
        """4x4 matrix representation w*1 + x*I + y*J + z*K.

        For a medium-state biquaternion (tau, i*alpha, i*beta, i*gamma) this
        is exactly the Z matrix (arXiv:1705.07147, Eq. (13)); for a Stokes
        biquaternion (s0, i*s1, i*s2, i*s3) it is the Stokes matrix S.
        """
        return (
            self.w * Q_ONE + self.x * Q_I + self.y * Q_J + self.z * Q_K
        )

    def simplify(self) -> "BiQuaternion":
        return BiQuaternion(
            sp.simplify(self.w),
            sp.simplify(self.x),
            sp.simplify(self.y),
            sp.simplify(self.z),
        )

    def equals(self, other: "BiQuaternion") -> bool:
        """Symbolic equality of all four components."""
        return all(
            sp.simplify(sp.expand(a - b)) == 0
            for a, b in (
                (self.w, other.w),
                (self.x, other.x),
                (self.y, other.y),
                (self.z, other.z),
            )
        )
