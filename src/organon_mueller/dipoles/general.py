"""General-geometry dimer + reciprocity (Symmetry 12, 1790 (2020), App. A).

Geometry: dipole 1 VERTICAL (along y) at the origin; dipole 2 at angle
theta in the xy plane, positioned at r = d*u with u = (C1C2, S1, C1S2)
(C_i = cos phi_i, S_i = sin phi_i). Plane wave along +z; e1 = e^{ikd}
(inter-dipole path phase), e2 = e^{ik r_z} (drive-phase of dipole 2).

NAMING WARNING (K33): the Symmetry paper's coupling scalars
delta1_s = k^2 (A + S1^2 B), delta2_s = k^2 (C1 C2 S1 B) are DIFFERENT
objects from the PRB 98,045410 delta1 = k^2 A, delta2 = k^2 (A+B) used
in `dimer.py` — same letters in the papers, different meanings; here
they carry the `_s` suffix.

Far-field bookkeeping (probe-resolved, stage-13 Q1): the paper's
Eq. (A11) corresponds to T = e2*p1 + p2 — i.e. the single-particle
terms carry e2 (dipole 2 sits r_z closer to the +z detector; the
overall path factor is absorbed in F).

M28: `forward_jones_general` is DERIVED from the scalar-reduced coupled
system; Eq. (A11) is only an anchor in tests (K28).
"""
from __future__ import annotations

import sympy as sp

from .dimer import jones_to_hvector

__all__ = [
    "coupling_matrix",
    "symmetry_deltas",
    "solve_dimer_general",
    "forward_jones_general",
    "reciprocity_transform",
    "case_A_jones",
    "case_B_jones",
    "forward_gamma_general",
    "forward_jones_numeric",
]

_SIGMA = sp.diag(1, -1)


def coupling_matrix(phi1, phi2, a_coef, b_coef, e1) -> sp.Matrix:
    """M = e1 (A I + B w w^T) on xy components, w = (C1 C2, S1) — the
    xy-projection of the unit separation vector (Green function, M28)."""
    w = sp.Matrix([sp.cos(phi1) * sp.cos(phi2), sp.sin(phi1)])
    return e1 * (a_coef * sp.eye(2) + b_coef * w * w.T)


def symmetry_deltas(theta, phi1, phi2, a_coef, b_coef):
    """The paper's coupling scalars (K33 `_s` naming): delta1_s =
    A + S1^2 B, delta2_s = C1 C2 S1 B (k^2 absorbed into A, B) and the
    interaction coefficients Delta1 = b*delta1_s + a*delta2_s,
    Delta2 = c*delta1_s + b*delta2_s (a, b, c from theta)."""
    s1 = sp.sin(phi1)
    d1s = a_coef + s1 ** 2 * b_coef
    d2s = sp.cos(phi1) * sp.cos(phi2) * s1 * b_coef
    a_, b_, c_ = (sp.cos(theta) ** 2, sp.cos(theta) * sp.sin(theta),
                  sp.sin(theta) ** 2)
    return d1s, d2s, b_ * d1s + a_ * d2s, c_ * d1s + b_ * d2s


def solve_dimer_general(theta, phi1, phi2, alpha1, alpha2, a_coef, b_coef,
                        e1, e2, e0):
    """Scalar-reduced coupled solve (probe Q2): p1 = P1*yhat, p2 =
    P2*n(theta); coupling scalars c_ij = n_i^T M n_j (M symmetric).
    Drives: dipole 1 sees E0, dipole 2 sees e2*E0 (eps = 1)."""
    n1 = sp.Matrix([0, 1])
    n2 = sp.Matrix([sp.cos(theta), sp.sin(theta)])
    m = coupling_matrix(phi1, phi2, a_coef, b_coef, e1)
    c12 = (n1.T * m * n2)[0, 0]
    c21 = (n2.T * m * n1)[0, 0]
    e1drive = (n1.T * sp.Matrix(e0))[0, 0]
    e2drive = e2 * (n2.T * sp.Matrix(e0))[0, 0]
    den = 1 - alpha1 * alpha2 * c12 * c21
    p1 = alpha1 * (e1drive + alpha2 * c12 * e2drive) / den
    p2 = alpha2 * (e2drive + alpha1 * c21 * e1drive) / den
    return p1 * n1, p2 * n2


def forward_jones_general(theta, phi1, phi2, alpha1, alpha2, a_coef, b_coef,
                          e1, e2) -> sp.Matrix:
    """T for e(z)d(z): columns are e2*p1 + p2 for basis excitations
    (probe-resolved bookkeeping; anchored against Eq. A11)."""
    cols = []
    for e0 in ((1, 0), (0, 1)):
        p1, p2 = solve_dimer_general(theta, phi1, phi2, alpha1, alpha2,
                                     a_coef, b_coef, e1, e2, e0)
        cols.append(e2 * p1 + p2)
    return sp.simplify(sp.Matrix.hstack(*cols))


def reciprocity_transform(j: sp.Matrix) -> sp.Matrix:
    """Van de Hulst / paper Eq. (1): J -> sigma J^T sigma =
    [[j00, -j10], [-j01, j11]] (involutive)."""
    return _SIGMA * j.T * _SIGMA


def _case_scalars(alpha, b_coef, e1):
    """Shared Case-A/B machinery: phi1 = -45 deg, phi2 = 0, theta = 0,
    both dipoles in the z = 0 plane (e2 = 1). Coupling scalar c =
    yhat^T M xhat = -e1*B/2 = e1*delta (paper's delta = -k^2 B/2)."""
    delta = -b_coef / 2
    c = e1 * delta
    den = 1 - alpha ** 2 * c ** 2
    g = alpha / den            # eps = F = 1
    mu = e1 * alpha * delta
    return c, den, g, mu


def case_A_jones(alpha, b_coef, e1) -> sp.Matrix:
    """DERIVED Case A (excite +z, detect +x): only p_y radiates toward
    +x (transverse projection); local frame (H' from -z, V = y) gives
    row H' = 0. Anchor: g[[0,0],[mu,1]] (paper Eq. 6)."""
    c, den, _, _ = _case_scalars(alpha, b_coef, e1)
    row = []
    for e0 in (sp.Matrix([1, 0]), sp.Matrix([0, 1])):
        e1drive = e0[1]          # vertical dipole driven by E0y
        e2drive = e0[0]          # horizontal dipole (theta=0) by E0x
        p1 = alpha * (e1drive + alpha * c * e2drive) / den
        row.append(p1)
    return sp.simplify(sp.Matrix([[0, 0], row]))


def case_B_jones(alpha, b_coef, e1) -> sp.Matrix:
    """DERIVED Case B (excite -x, detect -z): H (= z-polarized) drives
    neither in-plane dipole; V drives dipole 1, which feeds dipole 2 via
    coupling; -z local frame flips the x axis (H' = -x). Anchor:
    g[[0,-mu],[0,1]] (paper Eq. 7)."""
    c, den, _, _ = _case_scalars(alpha, b_coef, e1)
    p1 = alpha / den                 # V drive on dipole 1
    p2 = alpha * (alpha * c) / den   # dipole 2 via coupling only
    return sp.simplify(sp.Matrix([[0, -p2], [0, p1]]))


def forward_gamma_general(theta, phi1, phi2, alpha1, alpha2, a_coef, b_coef,
                          e1, e2) -> sp.Expr:
    """gamma (4th covariance component) of the DERIVED forward J —
    theorem (tests): equals i*e1*alpha1*alpha2*Delta1*(1-e2^2)/(2N);
    vanishes iff no coupling, Delta1 = 0, or e2^2 = 1 (co-planar dimers
    and half-wavelength z-offsets are gamma-blind in forward scattering).
    """
    j = forward_jones_general(theta, phi1, phi2, alpha1, alpha2,
                              a_coef, b_coef, e1, e2)
    return sp.simplify(jones_to_hvector(j).gamma)


def forward_jones_numeric(theta, phi1, phi2, alpha1, alpha2, a_coef, b_coef,
                          e1, e2):
    """Numeric forward J with K26 guards (finite inputs; resonance N~0)."""
    import numpy as np

    vals = [complex(v) for v in (theta, phi1, phi2, alpha1, alpha2,
                                 a_coef, b_coef, e1, e2)]
    if not all(np.isfinite(v.real) and np.isfinite(v.imag) for v in vals):
        raise ValueError("non-finite dimer parameters")
    th, f1, f2, a1, a2, ac, bc, e1v, e2v = vals
    for label, ang in (("theta", th), ("phi1", f1), ("phi2", f2)):
        if abs(ang.imag) > 1e-12:  # review: no silent .real truncation
            raise ValueError(f"{label} must be a real angle, got {ang}")
    th, f1, f2 = th.real, f1.real, f2.real
    c1, s1, c2 = np.cos(f1), np.sin(f1), np.cos(f2)
    a_, b_, c_ = (np.cos(th) ** 2, np.cos(th) * np.sin(th),
                  np.sin(th) ** 2)
    d1s, d2s = ac + s1 ** 2 * bc, c1 * c2 * s1 * bc
    n = 1 - e1v ** 2 * a1 * a2 * (2 * b_ * d1s * d2s + c_ * d1s ** 2
                                  + a_ * d2s ** 2)
    if abs(n) < 1e-12:
        raise ValueError(f"on-resonance denominator N = {n} (hybrid mode); "
                         "scattering diverges")
    dd1 = b_ * d1s + a_ * d2s
    dd2 = c_ * d1s + b_ * d2s
    j1 = np.array([[0, 0], [0, 1.0]])
    j2 = np.array([[a_, b_], [b_, c_]])
    jint = np.array([[0, dd1], [e2v ** 2 * dd1, (1 + e2v ** 2) * dd2]])
    return (e2v * a1 * j1 + e2v * a2 * j2 + e1v * a1 * a2 * jint) / n
