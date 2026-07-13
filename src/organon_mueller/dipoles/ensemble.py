"""3D dimer + ensemble optical activity (Kuntman & Kuntman, OA-in-
ensemble preprint; M37).

3D rank-1 dipoles along unit vectors m, n separated by r (u = r/D);
plane wave along +z with drive phases e^{-+ik rz/2} (n behind m);
coupling scalar delta = (n.m)A + (n.u)(m.u)B (k^2 absorbed into A, B);
mu = eps*alpha/(1 - (alpha*delta)^2).

Conventions (K33): the paper's optical-activity parameter is
gamma = i(J12 - J21) = 2 * HVector.gamma (no 1/2) — exposed here as
`gamma_paper` to avoid confusion. Print notes (M30, probe-verified):
Eq. (31)'s cross product is (n x m)_z, printed "(m x n)_z"; Eq. (9)'s
prefactor is -2i*mu, printed "-2i*eps*alpha*mu" (mu already contains
eps*alpha). Bracket contents are correct in both. Further print
notes: Eq. (30) prints "i(J12 - J12)" (second should be J21); Eq. (32)
phases print e^{i rx/2} with the k dropped.

Rigid-dimer note: for a rigid dimer all dot products (n.m), (n.u),
(m.u) are rotation-invariant, so delta (and mu) are ensemble constants
— the paper's "mu, alpha and delta do not depend on the orientation".
"""
from __future__ import annotations

import numpy as np
import sympy as sp

__all__ = [
    "coupling_delta_3d",
    "solve_dimer_3d",
    "forward_jones_3d",
    "transverse_jones_3d",
    "backscatter_jones_3d",
    "gamma_paper",
    "is_chiral",
    "jones_3d_numeric",
    "ensemble_gamma",
    "ensemble_covariance",
]


def coupling_delta_3d(m, n, u, a_coef, b_coef):
    """delta = (n.m)A + (n.u)(m.u)B (Green dyadic on rank-1 axes, M28)."""
    dot = lambda x, y: sum(xi * yi for xi, yi in zip(x, y))  # noqa: E731
    return dot(n, m) * a_coef + dot(n, u) * dot(m, u) * b_coef


def solve_dimer_3d(m, n, rz, alpha, delta, ex, ey, k=1, eps=1):
    """Scalar amplitudes (Qn, Qm) with p_n = Qn*n, p_m = Qm*m — derived
    from the rank-1 reduction of Eqs. (11)-(12); anchored against the
    paper's Eqs. (21)-(24) in tests."""
    en = sp.exp(-sp.I * k * rz / 2) * (n[0] * ex + n[1] * ey)
    em = sp.exp(sp.I * k * rz / 2) * (m[0] * ex + m[1] * ey)
    mu = eps * alpha / (1 - (alpha * delta) ** 2)
    return mu * (en + em * alpha * delta), mu * (em + en * alpha * delta)


def _jones(m, n, rz, rx, alpha, delta, direction, k=1, eps=1) -> sp.Matrix:
    cols = []
    for ex, ey in ((1, 0), (0, 1)):
        qn, qm = solve_dimer_3d(m, n, rz, alpha, delta, ex, ey, k, eps)
        if direction == "+z":
            fn, fm = sp.exp(sp.I * k * rz / 2), sp.exp(-sp.I * k * rz / 2)
            cols.append(sp.Matrix([fn * qn * n[0] + fm * qm * m[0],
                                   fn * qn * n[1] + fm * qm * m[1]]))
        elif direction == "+x":
            fn, fm = sp.exp(sp.I * k * rx / 2), sp.exp(-sp.I * k * rx / 2)
            cols.append(sp.Matrix([-(fn * qn * n[2] + fm * qm * m[2]),
                                   fn * qn * n[1] + fm * qm * m[1]]))
        elif direction == "-z":
            fn, fm = sp.exp(-sp.I * k * rz / 2), sp.exp(sp.I * k * rz / 2)
            cols.append(sp.Matrix([-(fn * qn * n[0] + fm * qm * m[0]),
                                   fn * qn * n[1] + fm * qm * m[1]]))
        else:
            raise ValueError(f"unknown direction: {direction}")
    return sp.Matrix.hstack(*cols)


def forward_jones_3d(m, n, rz, alpha, delta, k=1, eps=1) -> sp.Matrix:
    """Forward (+z) Jones (anchor: paper Eqs. 26-29)."""
    return _jones(m, n, rz, 0, alpha, delta, "+z", k, eps)


def transverse_jones_3d(m, n, rz, rx, alpha, delta, k=1, eps=1) -> sp.Matrix:
    """+x-direction Jones: local frame x' = -z, y' = y, path phases rx
    (paper Eq. 32); gamma anchor Eq. 33."""
    return _jones(m, n, rz, rx, alpha, delta, "+x", k, eps)


def backscatter_jones_3d(m, n, rz, alpha, delta, k=1, eps=1) -> sp.Matrix:
    """-z-direction Jones (paper Eq. 8 frame: x' = -x, y' = y); gamma
    anchor is Eq. 9 with the CORRECTED -2i*mu prefactor (M30 #6)."""
    return _jones(m, n, rz, 0, alpha, delta, "-z", k, eps)


def gamma_paper(j: sp.Matrix):
    """Paper's OA parameter gamma = i(J12 - J21) = 2*HVector.gamma (K33)."""
    return sp.I * (j[0, 1] - j[1, 0])


def is_chiral(m, n, r, tol=1e-12) -> bool:
    """Geometry is chiral iff m, n, r are NOT coplanar: m x n . r != 0."""
    m, n, r = (np.asarray(v, dtype=float) for v in (m, n, r))
    return bool(abs(np.dot(np.cross(m, n), r)) > tol)


def jones_3d_numeric(m, n, r, alpha, a_coef, b_coef, direction="+z",
                     k=1.0, eps=1.0):
    """Numeric Jones with K26 guards (finite inputs, resonance)."""
    m = np.asarray(m, dtype=float)
    n = np.asarray(n, dtype=float)
    r = np.asarray(r, dtype=float)
    vals = [complex(alpha), complex(a_coef), complex(b_coef)]
    if not (np.all(np.isfinite(m)) and np.all(np.isfinite(n))
            and np.all(np.isfinite(r))
            and all(np.isfinite(v.real) and np.isfinite(v.imag)
                    for v in vals)):
        raise ValueError("non-finite ensemble-dimer parameters")
    d = float(np.linalg.norm(r))
    if d < 1e-12:
        raise ValueError("coincident dipoles (|r| = 0)")
    u = r / d
    delta = complex(coupling_delta_3d(m, n, u, a_coef, b_coef))
    den = 1 - (complex(alpha) * delta) ** 2
    if abs(den) < 1e-12:
        raise ValueError(f"on-resonance denominator 1-(alpha*delta)^2 = "
                         f"{den}; scattering diverges")
    j = _jones(tuple(m), tuple(n), float(r[2]), float(r[0]),
               complex(alpha), delta, direction, k, eps)
    return np.array(sp.matrix2numpy(j.evalf(), dtype=complex))


def _orthogonal_dimer(rng):
    """Random rigid orthogonal dimer (paper Fig. 2): m, n orthogonal in a
    random plane, z = plane normal."""
    u = rng.standard_normal(3)
    u /= np.linalg.norm(u)
    v = rng.standard_normal(3)
    v -= u * (u @ v)
    v /= np.linalg.norm(v)
    z = np.cross(u, v)
    mm = (u + v) / np.sqrt(2)
    nn = (u - v) / np.sqrt(2)
    return mm, nn, z


def ensemble_gamma(direction="+z", chiral=True, d=1.3,
                   alpha=0.4 + 0.2j, a_coef=0.25 + 0.1j, b_coef=-0.35 + 0.05j,
                   n_samples=800, seed=20260713):
    """Deterministic ensemble sums over random rigid orthogonal dimers
    (Fig. 2 geometry: r = d(m - n + z)/sqrt(3); achiral drops the z
    term). NOTE: this `d` is the full separation |r| (the paper's D);
    the paper's Fig-2 "d" is D/sqrt(3). Returns mean gamma, mean |gamma|
    (paper Eq. 2 statistics)."""
    rng = np.random.default_rng(seed)
    tot, tot_abs = 0j, 0.0
    for _ in range(n_samples):
        mm, nn, z = _orthogonal_dimer(rng)
        if chiral:
            r = d * (mm - nn + z) / np.sqrt(3)
        else:
            r = d * (mm - nn) / np.sqrt(2)
        j = jones_3d_numeric(mm, nn, r, alpha, a_coef, b_coef, direction)
        g = complex(1j * (j[0, 1] - j[1, 0]))
        tot += g
        tot_abs += abs(g)
    return {"mean_gamma": tot / n_samples,
            "mean_abs_gamma": tot_abs / n_samples,
            "n_samples": n_samples, "seed": seed, "chiral": chiral,
            "direction": direction, "d": d}


def ensemble_covariance(orientations, d=1.3, alpha=0.4 + 0.2j,
                        a_coef=0.25 + 0.1j, b_coef=-0.35 + 0.05j,
                        direction="+z", chiral=True):
    """Depolarization bridge (first end-to-end): the ensemble-averaged
    covariance <|h><h|> over the GIVEN orientation samples (each an
    (m, n, z) triple), trace-normalized. A finite mixture of K distinct
    orientations gives rank <= K — feedable to the decomposition layer
    (`propose_decompositions`), whose outcome is REASONED either way
    (K21). Uses OUR half-convention h (jones_to_hvector)."""
    if not orientations:
        raise ValueError("empty orientation sample (K26)")
    acc = np.zeros((4, 4), dtype=complex)
    for mm, nn, z in orientations:
        mm, nn, z = (np.asarray(v, dtype=float) for v in (mm, nn, z))
        r = d * (mm - nn + (z if chiral else 0)) / np.sqrt(3 if chiral else 2)
        j = jones_3d_numeric(mm, nn, r, alpha, a_coef, b_coef, direction)
        h = np.array([complex((j[0, 0] + j[1, 1]) / 2),
                      complex((j[0, 0] - j[1, 1]) / 2),
                      complex((j[0, 1] + j[1, 0]) / 2),
                      complex(1j * (j[0, 1] - j[1, 0]) / 2)])
        acc += np.outer(h, h.conj())
    acc /= len(orientations)
    trace = float(np.trace(acc).real)
    if trace < 1e-300:
        raise ValueError("zero ensemble covariance")
    return acc / trace
