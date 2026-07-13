"""The known-identity library (stage-00 seed) and its verification.

Each entry records the identity, its literature source, its side
conditions (Horn guards, decision M3) and a `check` callable that proves
it — symbolically where tractable, otherwise by deterministic random
sampling (decision M2).

This library doubles as the regression suite: recovering 14/14 known
identities is the stage-00 acceptance criterion, mirroring Organon v1's
"recover the known" discipline.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import sympy as sp

from ..algebra.states import (
    HVector,
    covariance_from_mueller,
    hvector_from_covariance,
    hvector_from_quaternion,
    mueller_from_covariance,
    mueller_from_jones,
    mueller_rotation,
    rotator_quaternion,
    stokes_from_quaternion,
    stokes_matrix,
    stokes_quaternion,
    z_from_jones,
    zstar_from_jones,
)
from ..conditions import covariance_rank, trace_condition
from ..verify import (
    numeric_equal,
    random_params,
    random_hvector,
    random_stokes,
    sample_check,
    symbolic_equal,
    symbolic_zero,
    to_numpy,
)

__all__ = ["Identity", "KNOWN_IDENTITIES", "verify_all"]


@dataclass(frozen=True)
class Identity:
    key: str
    statement: str
    source: str
    conditions: tuple[str, ...]
    mode: str  # "symbolic" | "numeric" | "symbolic+numeric"
    check: Callable[[], bool]


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def _check_i1() -> bool:
    """M = Z Z^* = Z^* Z, and M is real."""
    h = HVector.generic("a")
    z = h.to_z()
    m = sp.expand(z * z.conjugate())
    m_alt = sp.expand(z.conjugate() * z)
    return symbolic_equal(m, m_alt) and symbolic_equal(m, m.conjugate())


def _check_i2() -> bool:
    """Consistency of the Jones route: M = A(J kron J^*)A^{-1} = Z Z^*."""
    h = HVector.generic("a")
    jones = h.to_jones()
    ok_m = symbolic_equal(mueller_from_jones(jones), h.to_mueller())
    ok_z = symbolic_equal(z_from_jones(jones), h.to_z())
    ok_zs = symbolic_equal(zstar_from_jones(jones), h.to_z().conjugate())
    return ok_m and ok_z and ok_zs


def _check_i3() -> bool:
    """det Z = (tau^2 - alpha^2 - beta^2 - gamma^2)^2."""
    h = HVector.generic("a")
    t, a, b, g = h.tau, h.alpha, h.beta, h.gamma
    det = h.to_z().det(method="berkowitz")
    return symbolic_zero(det - (t**2 - a**2 - b**2 - g**2) ** 2)


def _check_i4() -> bool:
    """Z^{-1} by sign flip: Z * Z_flip = (tau^2-alpha^2-beta^2-gamma^2) I."""
    h = HVector.generic("a")
    t, a, b, g = h.tau, h.alpha, h.beta, h.gamma
    z = h.to_z()
    z_flip = HVector(t, -a, -b, -g).to_z()
    lhs = sp.expand(z * z_flip)
    rhs = sp.expand((t**2 - a**2 - b**2 - g**2) * sp.eye(4))
    return symbolic_equal(lhs, rhs)


def _check_i5() -> bool:
    """<h|h> = M00 = tau tau^* + alpha alpha^* + beta beta^* + gamma gamma^*."""
    h = HVector.generic("a")
    t, a, b, g = h.tau, h.alpha, h.beta, h.gamma
    m00 = h.to_mueller()[0, 0]
    norm = (
        t * sp.conjugate(t)
        + a * sp.conjugate(a)
        + b * sp.conjugate(b)
        + g * sp.conjugate(g)
    )
    return symbolic_zero(m00 - norm)


def _check_i6() -> bool:
    """Gil-Bernabeu trace condition tr(M^T M) = 4 M00^2 for pure states."""

    def one(rng: np.random.Generator) -> bool:
        m = to_numpy(random_hvector(rng).to_mueller())
        return trace_condition(m)

    return sample_check(one)


def _check_i7() -> bool:
    """Quaternion product maps to Z action: h2 h1 <-> Z2 |h1>."""
    ha, hb = HVector.generic("a"), HVector.generic("b")
    prod = hb.to_quaternion() * ha.to_quaternion()
    lhs = hvector_from_quaternion(prod).to_column()
    rhs = sp.expand(hb.to_z() * ha.to_column())
    return symbolic_equal(lhs, rhs)


def _check_i8() -> bool:
    """Matrix representation of the state quaternion equals Z."""
    h = HVector.generic("a")
    return symbolic_equal(h.to_quaternion().to_matrix(), h.to_z())


def _check_i9() -> bool:
    """Stokes transformation: s' = h s h^dag <-> |s'> = M|s>, S' = Z S Z^dag."""

    def one(rng: np.random.Generator) -> bool:
        h = random_hvector(rng)
        s = random_stokes(rng)
        hq = h.to_quaternion()
        sq = stokes_quaternion(s)
        s_out_q = hq * sq * hq.hermitian_conjugate()
        s_prime = to_numpy(stokes_from_quaternion(s_out_q))
        m = to_numpy(h.to_mueller())
        ok_vec = numeric_equal(s_prime.flatten(), m @ np.array(s, dtype=complex))
        z = to_numpy(h.to_z())
        s_mat = to_numpy(stokes_matrix(s))
        s_mat_prime = to_numpy(stokes_matrix([complex(v) for v in s_prime.flatten()]))
        ok_mat = numeric_equal(z @ s_mat @ z.conj().T, s_mat_prime)
        return ok_vec and ok_mat

    return sample_check(one, samples=25)


def _check_i10() -> bool:
    """Z_a Z_b^* = Z_b^* Z_a, hence M(Z2 Z1) = M2 M1 (serial combination)."""
    ha, hb = HVector.generic("a"), HVector.generic("b")
    za, zb = ha.to_z(), hb.to_z()
    ok_comm = symbolic_equal(
        sp.expand(za * zb.conjugate()), sp.expand(zb.conjugate() * za)
    )

    def one(rng: np.random.Generator) -> bool:
        h1, h2 = random_hvector(rng), random_hvector(rng)
        z1, z2 = to_numpy(h1.to_z()), to_numpy(h2.to_z())
        z21 = z2 @ z1
        m_serial = z21 @ z21.conj()
        m_product = to_numpy(h2.to_mueller()) @ to_numpy(h1.to_mueller())
        return numeric_equal(m_serial, m_product)

    return ok_comm and sample_check(one, samples=25)


def _check_i11() -> bool:
    """Rotations: |h(t)> = R(t)|h>, h(t) = r h r^dag, M(t) = R(t) M R(-t)."""

    def one(rng: np.random.Generator) -> bool:
        h = random_hvector(rng)
        theta = float(rng.uniform(0, 2 * np.pi))
        r4 = to_numpy(mueller_rotation(theta))
        h_col = to_numpy(h.to_column()).flatten()
        h_rot_col = r4 @ h_col
        h_rot = HVector(*[sp.sympify(complex(v)) for v in h_rot_col])
        # quaternion route
        r = rotator_quaternion(theta)
        q_rot = r * h.to_quaternion() * r.hermitian_conjugate()
        ok_q = numeric_equal(
            to_numpy(hvector_from_quaternion(q_rot).to_column()).flatten(),
            h_rot_col,
        )
        # Mueller route
        m_rot = to_numpy(h_rot.to_mueller())
        m_conj = r4 @ to_numpy(h.to_mueller()) @ to_numpy(mueller_rotation(-theta))
        return ok_q and numeric_equal(m_rot, m_conj)

    return sample_check(one, samples=25)


def _check_i12() -> bool:
    """Hermitian state (all parameters real) gives a symmetric Mueller matrix."""

    def one(rng: np.random.Generator) -> bool:
        t, a, b, g = (float(x) for x in rng.standard_normal(4))
        m = to_numpy(HVector(*(sp.sympify(v) for v in (t, a, b, g))).to_mueller())
        return numeric_equal(m, m.T)

    return sample_check(one)


def _check_i13() -> bool:
    """Unitary state (tau real; alpha,beta,gamma imaginary): M M^T = M00^2 I."""

    def one(rng: np.random.Generator) -> bool:
        t = float(rng.standard_normal())
        a, b, g = (sp.I * sp.sympify(float(x)) for x in rng.standard_normal(3))
        m = to_numpy(HVector(sp.sympify(t), a, b, g).to_mueller())
        return numeric_equal(m @ m.T, (m[0, 0] ** 2) * np.eye(4))

    return sample_check(one)


def _check_i14() -> bool:
    """Covariance route: H = |h><h| has rank 1; M_ij = tr(Pi_ij H); h recoverable."""

    def one(rng: np.random.Generator) -> bool:
        h = random_hvector(rng)
        m = h.to_mueller()
        cov = covariance_from_mueller(m)
        ok_rank = covariance_rank(to_numpy(cov)) == 1
        ok_round = numeric_equal(to_numpy(mueller_from_covariance(cov)), to_numpy(m))
        ok_outer = numeric_equal(to_numpy(cov), to_numpy(h.to_covariance_matrix()))
        h_rec = hvector_from_covariance(cov)
        ok_h = numeric_equal(
            to_numpy(h_rec.to_covariance_matrix()), to_numpy(cov)
        )
        return ok_rank and ok_round and ok_outer and ok_h

    return sample_check(one, samples=25)


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------

KNOWN_IDENTITIES: tuple[Identity, ...] = (
    Identity(
        "I1", "M = Z Z^* = Z^* Z and M is real",
        "Kuntman-Kuntman-Arteaga, JOSA A 34, 80 (2017), Eq. (34)",
        ("nondepolarizing",), "symbolic", _check_i1,
    ),
    Identity(
        "I2", "M = A (J kron J^*) A^{-1} consistent with Z-route; Z = A(J kron I)A^{-1}",
        "JOSA A 34, 80 (2017), Eq. (35)",
        (), "symbolic", _check_i2,
    ),
    Identity(
        "I3", "det Z = (tau^2 - alpha^2 - beta^2 - gamma^2)^2",
        "JOSA A 34, 80 (2017), Eq. (48)",
        (), "symbolic", _check_i3,
    ),
    Identity(
        "I4", "Z^{-1} = sign-flipped Z / (tau^2-alpha^2-beta^2-gamma^2)",
        "JOSA A 34, 80 (2017), Eq. (50)",
        ("det_nonzero",), "symbolic", _check_i4,
    ),
    Identity(
        "I5", "<h|h> = M00",
        "JOSA A 34, 80 (2017), Eq. (17)",
        (), "symbolic", _check_i5,
    ),
    Identity(
        "I6", "tr(M^T M) = 4 M00^2",
        "Gil-Bernabeu (1985); JOSA A 34, 80 (2017), Sec. 4",
        ("nondepolarizing",), "numeric", _check_i6,
    ),
    Identity(
        "I7", "h2 h1 corresponds to Z2 |h1> (quaternion product = Z action)",
        "arXiv:1705.07147, Eqs. (21)-(23)",
        (), "symbolic", _check_i7,
    ),
    Identity(
        "I8", "Z = tau 1 + i alpha I + i beta J + i gamma K (matrix rep of h)",
        "arXiv:1705.07147, Eq. (13)",
        (), "symbolic", _check_i8,
    ),
    Identity(
        "I9", "s' = h s h^dag equivalent to |s'> = M |s> and S' = Z S Z^dag",
        "arXiv:1705.07147, Eqs. (10), (26)",
        (), "numeric", _check_i9,
    ),
    Identity(
        "I10", "Z_a Z_b^* = Z_b^* Z_a; M(Z2 Z1) = M2 M1",
        "JOSA A 34, 80 (2017), Eqs. (37)-(38)",
        (), "symbolic+numeric", _check_i10,
    ),
    Identity(
        "I11", "|h(t)> = R(t)|h>; h(t) = r h r^dag; M(t) = R(t) M R(-t)",
        "arXiv:1705.07147, Eqs. (30)-(34)",
        (), "numeric", _check_i11,
    ),
    Identity(
        "I12", "real parameters => M symmetric (Hermitian Z, diattenuator)",
        "JOSA A 34, 80 (2017), Eqs. (52)-(53)",
        ("hermitian_state",), "numeric", _check_i12,
    ),
    Identity(
        "I13", "tau real, alpha/beta/gamma imaginary => M M^T = M00^2 I (retarder)",
        "JOSA A 34, 80 (2017), Eqs. (54)-(56)",
        ("unitary_state",), "numeric", _check_i13,
    ),
    Identity(
        "I14", "rank(H)=1 for pure states; M_ij = tr(Pi_ij H); H = |h><h|",
        "Cloude (1986); Gil (2014); JOSA A 34, 80 (2017), Eqs. (6)-(9)",
        (), "numeric", _check_i14,
    ),
)


def verify_all() -> dict[str, bool]:
    """Run every known-identity check; returns {key: passed}."""
    return {identity.key: identity.check() for identity in KNOWN_IDENTITIES}
