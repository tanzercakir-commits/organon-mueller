"""Dimer scattering: the PRB 98, 045410 geometry (Fig. 1 — both dipoles
in the same z plane, dimer axis along y, plane-wave in-phase excitation,
equidistant far-field detector on the z axis).

M28 discipline: `scattering_matrix_direct` DERIVES T by solving the
coupled 4x4 system symbolically; `scattering_matrix_decomposed` writes
the paper's three-term form (Eq. 25). Their exact symbolic equality is
the stage's central anchor theorem (tests). Coupling scalars: delta1 =
k^2*A (transverse, x here) and delta2 = k^2*(A+B) (along the dimer
axis, y here); both stay OPAQUE symbols at this layer.

Conventions (K33): every anchor cites its equation number. Print-factor
note (M30): Eq. (37) of the paper is printed at 2x the scale of its own
Eq. (29) half-convention; the consistent fourth component is
h4 = -(i/2) sin(phi1-phi2) (1 - e^{i chi}) — directional claims (zero
iff chi=0 or phi1=phi2; purely circular at chi=pi) are unaffected.
"""
from __future__ import annotations

import sympy as sp

from ..algebra.states import HVector

__all__ = [
    "jones_projector",
    "interaction_jones",
    "dephased_interaction_jones",
    "coupling_lambda",
    "scattering_matrix_direct",
    "scattering_matrix_decomposed",
    "jones_to_hvector",
]


def jones_projector(phi) -> sp.Matrix:
    """Fully anisotropic dipole = projector onto direction phi (Eq. 9-12)."""
    c, s = sp.cos(phi), sp.sin(phi)
    return sp.Matrix([[c * c, c * s], [c * s, s * s]])


def coupling_lambda(phi1, phi2, delta1, delta2) -> sp.Expr:
    """Lambda = C1 C2 delta1 + S1 S2 delta2 (Eq. 20) — the ONLY coupling."""
    return (sp.cos(phi1) * sp.cos(phi2) * delta1
            + sp.sin(phi1) * sp.sin(phi2) * delta2)


def interaction_jones(phi1, phi2) -> sp.Matrix:
    """J_int (Eq. 27)."""
    c1, s1 = sp.cos(phi1), sp.sin(phi1)
    c2, s2 = sp.cos(phi2), sp.sin(phi2)
    return sp.Matrix([
        [2 * c1 * c2, c1 * s2 + c2 * s1],
        [c1 * s2 + c2 * s1, 2 * s1 * s2],
    ])


def dephased_interaction_jones(phi1, phi2, chi) -> sp.Matrix:
    """J'_int for a non-equidistant detector (Eq. 36); chi is the extra
    phase of dipole 2's path. The A13 optical-activity mechanism lives in
    this matrix's antisymmetric part."""
    c1, s1 = sp.cos(phi1), sp.sin(phi1)
    c2, s2 = sp.cos(phi2), sp.sin(phi2)
    e = sp.exp(sp.I * chi)
    return sp.Matrix([
        [c1 * c2 * (1 + e), c1 * s2 + c2 * s1 * e],
        [c1 * s2 * e + c2 * s1, s1 * s2 * (1 + e)],
    ])


def scattering_matrix_direct(phi1, phi2, alpha1, alpha2, delta1, delta2,
                             eps=1, beta=1) -> sp.Matrix:
    """DERIVE T from the coupled system (Eqs. 2-3 / 13 / 38), M28-style.

    p_i = alpha_i J_i [eps E0 + K p_j] with (K p)_x = delta1 p_x,
    (K p)_y = delta2 p_y (dimer axis along y). Solved with sympy
    linear_eq_to_matrix + LUsolve for each excitation basis vector;
    T columns are the scattered fields E_scat = beta (p1 + p2)."""
    j1, j2 = jones_projector(phi1), jones_projector(phi2)
    kmat = sp.diag(delta1, delta2)
    p = sp.Matrix(sp.symbols("p1x_d p1y_d p2x_d p2y_d", complex=True))
    p1, p2 = p[:2, 0], p[2:, 0]

    cols = []
    for e0 in (sp.Matrix([1, 0]), sp.Matrix([0, 1])):
        eqs = list(p1 - alpha1 * j1 * (eps * e0 + kmat * p2))
        eqs += list(p2 - alpha2 * j2 * (eps * e0 + kmat * p1))
        amat, rhs = sp.linear_eq_to_matrix(eqs, list(p))
        sol = amat.LUsolve(rhs)
        cols.append(beta * (sol[:2, 0] + sol[2:, 0]))
    return sp.simplify(sp.Matrix.hstack(*cols))


def scattering_matrix_decomposed(phi1, phi2, alpha1, alpha2, delta1, delta2,
                                 eps=1, beta=1) -> sp.Matrix:
    """The paper's three-term form (Eq. 25): T = gamma [alpha1 J1 +
    alpha2 J2 + alpha1 alpha2 Lambda J_int], gamma = eps beta / (1 -
    alpha1 alpha2 Lambda^2)."""
    lam = coupling_lambda(phi1, phi2, delta1, delta2)
    gamma = eps * beta / (1 - alpha1 * alpha2 * lam ** 2)
    return gamma * (alpha1 * jones_projector(phi1)
                    + alpha2 * jones_projector(phi2)
                    + alpha1 * alpha2 * lam * interaction_jones(phi1, phi2))


def scattering_matrix_numeric(phi1, phi2, alpha1, alpha2, delta1, delta2,
                              eps=1.0, beta=1.0):
    """Numeric evaluation of Eq. (25) with K26 guards (finite inputs;
    resonance denominator |1 - a1 a2 Lambda^2| must not vanish)."""
    import numpy as np

    vals = [complex(v) for v in (alpha1, alpha2, delta1, delta2, eps, beta,
                                 phi1, phi2)]  # angles too (review defect 1)
    if not all(np.isfinite(v.real) and np.isfinite(v.imag) for v in vals):
        raise ValueError("non-finite dipole parameters")
    a1, a2, d1, d2, ep, be = vals[:6]
    c1, s1 = np.cos(float(phi1)), np.sin(float(phi1))
    c2, s2 = np.cos(float(phi2)), np.sin(float(phi2))
    lam = c1 * c2 * d1 + s1 * s2 * d2
    den = 1 - a1 * a2 * lam ** 2
    if abs(den) < 1e-12:
        raise ValueError(
            f"on-resonance denominator 1 - a1 a2 Lambda^2 = {den} "
            "(hybrid mode condition, Eq. 43); scattering diverges")
    j1 = np.array([[c1 * c1, c1 * s1], [c1 * s1, s1 * s1]])
    j2 = np.array([[c2 * c2, c2 * s2], [c2 * s2, s2 * s2]])
    jint = np.array([[2 * c1 * c2, c1 * s2 + c2 * s1],
                     [c1 * s2 + c2 * s1, 2 * s1 * s2]])
    return (ep * be / den) * (a1 * j1 + a2 * j2 + a1 * a2 * lam * jint)


def jones_to_hvector(j: sp.Matrix) -> HVector:
    """Covariance vector of a Jones matrix (paper Eq. 29) — identical to
    the JOSA A 34, 80 convention of `HVector.to_jones` (sentinel-tested):
    (tau, alpha, beta, gamma) = ((j00+j11)/2, (j00-j11)/2, (j01+j10)/2,
    i(j01-j10)/2)."""
    return HVector(
        (j[0, 0] + j[1, 1]) / 2,
        (j[0, 0] - j[1, 1]) / 2,
        (j[0, 1] + j[1, 0]) / 2,
        sp.I * (j[0, 1] - j[1, 0]) / 2,
    )
