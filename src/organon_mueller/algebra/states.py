"""State representations of nondepolarizing optical media and conversions.

The internal source of truth is the covariance-vector parameter set
(tau, alpha, beta, gamma) (architectural decision M1 of stage-00).  All six
isomorphic representations are generated from it:

* Jones matrix          J = tau*s0 + alpha*s1 + beta*s2 + gamma*s3
* covariance vector     |h> = (tau, alpha, beta, gamma)^T
* covariance matrix     H = |h><h|
* Z matrix              (JOSA A 34, 80 (2017), Eq. (33))
* biquaternion          h = tau*1 + i*alpha*i + i*beta*j + i*gamma*k
* Mueller matrix        M = Z Z^*  (elementwise conjugate, NOT transpose)

Sources: E. Kuntman, M. A. Kuntman, O. Arteaga, JOSA A 34, 80 (2017);
E. Kuntman et al., arXiv:1705.07147 (quaternions).
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .basis import A, A_INV, PI, SIGMA
from .quaternion import BiQuaternion

__all__ = [
    "HVector",
    "hvector_from_jones",
    "hvector_from_quaternion",
    "hvector_from_covariance",
    "z_from_jones",
    "zstar_from_jones",
    "mueller_from_jones",
    "covariance_from_mueller",
    "mueller_from_covariance",
    "stokes_quaternion",
    "stokes_from_quaternion",
    "stokes_matrix",
    "mueller_rotation",
    "rotator_quaternion",
]

_i = sp.I


@dataclass(frozen=True)
class HVector:
    """Covariance vector |h> = (tau, alpha, beta, gamma)^T of a pure state."""

    tau: sp.Expr
    alpha: sp.Expr
    beta: sp.Expr
    gamma: sp.Expr

    def __post_init__(self) -> None:
        for name in ("tau", "alpha", "beta", "gamma"):
            object.__setattr__(self, name, sp.sympify(getattr(self, name)))

    @staticmethod
    def generic(prefix: str) -> "HVector":
        """Fresh generic complex parameters, e.g. HVector.generic('a')."""
        t, a, b, g = sp.symbols(
            f"tau_{prefix} alpha_{prefix} beta_{prefix} gamma_{prefix}",
            complex=True,
        )
        return HVector(t, a, b, g)

    # -- representations --------------------------------------------------
    def to_column(self) -> sp.Matrix:
        return sp.Matrix([self.tau, self.alpha, self.beta, self.gamma])

    def to_jones(self) -> sp.Matrix:
        """J = tau*sigma0 + alpha*sigma1 + beta*sigma2 + gamma*sigma3."""
        return (
            self.tau * SIGMA[0]
            + self.alpha * SIGMA[1]
            + self.beta * SIGMA[2]
            + self.gamma * SIGMA[3]
        )

    def to_z(self) -> sp.Matrix:
        """Explicit Z matrix (JOSA A 34, 80, Eq. (33))."""
        t, a, b, g = self.tau, self.alpha, self.beta, self.gamma
        return sp.Matrix(
            [
                [t, a, b, g],
                [a, t, -_i * g, _i * b],
                [b, _i * g, t, -_i * a],
                [g, -_i * b, _i * a, t],
            ]
        )

    def to_quaternion(self) -> BiQuaternion:
        """h = tau*1 + (i alpha)*i + (i beta)*j + (i gamma)*k."""
        return BiQuaternion(
            self.tau, _i * self.alpha, _i * self.beta, _i * self.gamma
        )

    def to_mueller(self) -> sp.Matrix:
        """M = Z Z^* (elementwise conjugate)."""
        z = self.to_z()
        return sp.expand(z * z.conjugate())

    def to_covariance_matrix(self) -> sp.Matrix:
        """H = |h><h| (rank 1, positive semidefinite)."""
        col = self.to_column()
        return col * col.H

    # -- helpers -----------------------------------------------------------
    def subs(self, mapping) -> "HVector":
        return HVector(
            self.tau.subs(mapping),
            self.alpha.subs(mapping),
            self.beta.subs(mapping),
            self.gamma.subs(mapping),
        )


# -- reverse conversions ----------------------------------------------------

def hvector_from_jones(jones: sp.Matrix) -> HVector:
    """Invert J = tau*s0 + alpha*s1 + beta*s2 + gamma*s3."""
    return HVector(
        tau=sp.expand((jones[0, 0] + jones[1, 1]) / 2),
        alpha=sp.expand((jones[0, 0] - jones[1, 1]) / 2),
        beta=sp.expand((jones[0, 1] + jones[1, 0]) / 2),
        gamma=sp.expand(_i * (jones[0, 1] - jones[1, 0]) / 2),
    )


def hvector_from_quaternion(q: BiQuaternion) -> HVector:
    """Invert h = tau*1 + i*alpha*i + i*beta*j + i*gamma*k."""
    return HVector(
        tau=sp.expand(q.w),
        alpha=sp.expand(-_i * q.x),
        beta=sp.expand(-_i * q.y),
        gamma=sp.expand(-_i * q.z),
    )


def hvector_from_covariance(cov: sp.Matrix) -> HVector:
    """Recover |h> from a rank-1 covariance matrix H = |h><h|.

    Uses the global-phase convention tau real and positive, in which case
    h = H[:, 0] / sqrt(H[0, 0]).  Requires tau != 0; the tau = 0 symmetry
    classes (Class 1 generators alpha/beta/gamma etc.) are deferred to
    later stages, and passing one raises instead of silently returning
    a zero state.
    """
    h00 = cov[0, 0]
    trace = sp.trace(cov)
    degenerate = bool(h00.is_zero)
    if not degenerate and h00.is_number and trace.is_number:
        scale = max(abs(complex(trace)), 1.0e-300)
        degenerate = abs(complex(h00)) <= 1.0e-12 * scale
    if degenerate:
        raise ValueError(
            "hvector_from_covariance requires H[0,0] != 0 (tau != 0 "
            "convention); tau = 0 symmetry classes are out of stage-00 scope"
        )
    col = cov[:, 0] / sp.sqrt(h00)
    return HVector(col[0], col[1], col[2], col[3])


# -- Jones-side constructions ------------------------------------------------

def z_from_jones(jones: sp.Matrix) -> sp.Matrix:
    """Z = A (J kron I) A^{-1}  (JOSA A 34, 80, Eq. (35))."""
    kron = sp.Matrix(sp.kronecker_product(jones, sp.eye(2)))
    return sp.expand(A * kron * A_INV)


def zstar_from_jones(jones: sp.Matrix) -> sp.Matrix:
    """Z^* = A (I kron J^*) A^{-1}  (JOSA A 34, 80, Eq. (35))."""
    kron = sp.Matrix(sp.kronecker_product(sp.eye(2), jones.conjugate()))
    return sp.expand(A * kron * A_INV)


def mueller_from_jones(jones: sp.Matrix) -> sp.Matrix:
    """Mueller-Jones matrix M = A (J kron J^*) A^{-1}."""
    kron = sp.Matrix(sp.kronecker_product(jones, jones.conjugate()))
    return sp.expand(A * kron * A_INV)


# -- Mueller <-> covariance ----------------------------------------------------

def covariance_from_mueller(mueller: sp.Matrix) -> sp.Matrix:
    """H = (1/4) sum_ij M_ij Pi_ij  (JOSA A 34, 80, Eq. (6))."""
    acc = sp.zeros(4, 4)
    for i in range(4):
        for j in range(4):
            acc += mueller[i, j] * PI[i][j]
    return sp.expand(acc / 4)


def mueller_from_covariance(cov: sp.Matrix) -> sp.Matrix:
    """M_ij = tr(Pi_ij H)  (JOSA A 34, 80, Eq. (8))."""
    return sp.Matrix(
        4, 4, lambda i, j: sp.expand(sp.trace(PI[i][j] * cov))
    )


# -- Stokes side ---------------------------------------------------------------

def stokes_quaternion(s) -> BiQuaternion:
    """s = s0*1 + i*s1*i + i*s2*j + i*s3*k  (arXiv:1705.07147, Eq. (28))."""
    s0, s1, s2, s3 = s
    return BiQuaternion(s0, _i * s1, _i * s2, _i * s3)


def stokes_from_quaternion(q: BiQuaternion) -> sp.Matrix:
    """Inverse of :func:`stokes_quaternion` (column vector)."""
    return sp.Matrix(
        [sp.expand(q.w), sp.expand(-_i * q.x), sp.expand(-_i * q.y), sp.expand(-_i * q.z)]
    )


def stokes_matrix(s) -> sp.Matrix:
    """Stokes matrix S (arXiv:1705.07147, Eq. (11)) via the quaternion rep."""
    return stokes_quaternion(s).to_matrix()


# -- rotations ------------------------------------------------------------------

def mueller_rotation(theta) -> sp.Matrix:
    """Mueller-space rotator R(theta) (note the 2*theta; Eq. (31))."""
    c, s = sp.cos(2 * theta), sp.sin(2 * theta)
    return sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1],
        ]
    )


def rotator_quaternion(theta) -> BiQuaternion:
    """r = cos(theta)*1 + sin(theta)*k  (arXiv:1705.07147, Eq. (33))."""
    return BiQuaternion(sp.cos(theta), 0, 0, sp.sin(theta))
