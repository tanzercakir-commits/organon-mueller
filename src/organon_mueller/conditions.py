"""Predicates (guards) on states and Mueller matrices.

These are the seed of the Horn-conditional rule layer (stage-00 decision
M3): identities in the library carry condition keys that map to the
predicates below.
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "CONDITIONS",
    "trace_condition",
    "covariance_rank",
    "is_nondepolarizing_mueller",
    "is_hermitian_state",
    "is_unitary_state",
    "has_nonzero_det_params",
]

#: relative tolerance used across numeric predicates
RTOL = 1e-9


def trace_condition(mueller: np.ndarray, rtol: float = RTOL) -> bool:
    """Gil-Bernabeu trace condition tr(M^T M) = 4 M00^2 (nondepolarizing)."""
    m = np.asarray(mueller, dtype=complex)
    lhs = np.trace(m.T @ m)
    rhs = 4 * m[0, 0] ** 2
    scale = max(abs(lhs), abs(rhs), 1e-300)
    return bool(abs(lhs - rhs) / scale < rtol)


def covariance_rank(cov: np.ndarray, rtol: float = RTOL) -> int:
    """Numeric rank of a covariance matrix, relative to its largest eigenvalue.

    Stage-00 warning 3: the threshold is relative (rtol * lambda_max),
    never absolute.
    """
    h = np.asarray(cov, dtype=complex)
    eigvals = np.linalg.eigvalsh((h + h.conj().T) / 2)
    lam_max = float(np.max(np.abs(eigvals)))
    if lam_max == 0.0:
        return 0
    return int(np.sum(np.abs(eigvals) > rtol * lam_max))


def is_nondepolarizing_mueller(
    mueller: np.ndarray, cov: np.ndarray, rtol: float = RTOL
) -> bool:
    """Nondepolarizing iff rank(H) == 1; cross-checked with the trace condition."""
    return covariance_rank(cov, rtol) == 1 and trace_condition(mueller, rtol)


def is_hermitian_state(params, rtol: float = RTOL) -> bool:
    """tau, alpha, beta, gamma all real (diattenuator; M symmetric)."""
    return all(abs(complex(p).imag) <= rtol * (1 + abs(complex(p))) for p in params)


def is_unitary_state(params, rtol: float = RTOL) -> bool:
    """tau real and alpha, beta, gamma pure imaginary (retarder; M orthogonal)."""
    tau, alpha, beta, gamma = (complex(p) for p in params)
    ok_tau = abs(tau.imag) <= rtol * (1 + abs(tau))
    ok_vec = all(
        abs(p.real) <= rtol * (1 + abs(p)) for p in (alpha, beta, gamma)
    )
    return ok_tau and ok_vec


def has_nonzero_det_params(params, rtol: float = RTOL) -> bool:
    """det Z != 0, i.e. tau^2 - alpha^2 - beta^2 - gamma^2 != 0 (not a pure polarizer)."""
    tau, alpha, beta, gamma = (complex(p) for p in params)
    val = tau**2 - alpha**2 - beta**2 - gamma**2
    scale = 1 + max(abs(tau), abs(alpha), abs(beta), abs(gamma)) ** 2
    return abs(val) > rtol * scale


#: Registered guard vocabulary for the identity library (Horn-condition seed).
#: Every Identity.conditions key must appear here (enforced by tests).
CONDITIONS = {
    "nondepolarizing": is_nondepolarizing_mueller,
    "det_nonzero": has_nonzero_det_params,
    "hermitian_state": is_hermitian_state,
    "unitary_state": is_unitary_state,
}
