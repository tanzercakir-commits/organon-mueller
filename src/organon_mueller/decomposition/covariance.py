"""Standard-basis covariance matrix (AO2016 convention) and the symmetry
templates of Table 1.

CONVENTION WARNING (decision M29): Kuntman & Arteaga, Appl. Opt. 55, 2543
(2016) define H = (1/4) sum m_ij (sigma_i kron sigma_j) with
m_ij = tr[(sigma_i kron sigma_j) H] — the STANDARD basis, with NO conjugate
on sigma_j. This is a DIFFERENT object from the core's Pi-basis
`covariance_from_mueller`; the two must never be mixed (tests enforce the
distinction).
"""
from __future__ import annotations

import sympy as sp

from ..algebra.basis import SIGMA

__all__ = [
    "standard_covariance_from_mueller",
    "mueller_from_standard_covariance",
    "TYPE1", "TYPE2", "TYPE3",
    "SYMMETRY_TEMPLATES",
]


def _kron(i: int, j: int) -> sp.Matrix:
    return sp.Matrix(sp.kronecker_product(SIGMA[i], SIGMA[j]))


def _reshuffle(matrix: sp.Matrix) -> sp.Matrix:
    """Index reshuffle R(X)[(2a+b),(2c+d)] = X[(2a+d),(2c+b)] (involutive).

    CONVENTION — PROVEN (stage-8 review): R(P kron Q) = P kron Q^T for
    2x2 blocks, and Pauli matrices are Hermitian (sigma^T = sigma^*), so
    R((1/4) sum m_ij sigma_i kron sigma_j) = (1/4) sum m_ij sigma_i kron
    sigma_j^* — i.e. this module computes the STANDARD Cloude/Gil
    covariance; AO2016's printed Eq. (2) merely omits the conjugate (read
    literally it gives a non-PSD cousin). Verified against the paper's
    Eq. (17) numeric example entry-by-entry, with one caveat: the printed
    h03 imaginary part 0.0161 is a typesetting artifact of 0.1608 (the
    printed value is inconsistent with the paper's OWN derived Eqs.
    (18)-(20), which our pipeline reproduces exactly; Eq. (21)'s [1,3]
    entry carries a second such artifact).
    """
    def entry(r, c):
        a, b = divmod(r, 2)
        cc, d = divmod(c, 2)
        return matrix[2 * a + d, 2 * cc + b]

    return sp.Matrix(4, 4, entry)


def standard_covariance_from_mueller(mueller: sp.Matrix) -> sp.Matrix:
    """AO2016 covariance H (paper convention; see _reshuffle docstring)."""
    acc = sp.zeros(4, 4)
    for i in range(4):
        for j in range(4):
            acc += mueller[i, j] * _kron(i, j)
    return _reshuffle(sp.expand(acc / 4))


def mueller_from_standard_covariance(cov: sp.Matrix) -> sp.Matrix:
    """m_ij = tr[(sigma_i kron sigma_j) R(H)]  (inverse of the above)."""
    unshuffled = _reshuffle(cov)
    return sp.Matrix(
        4, 4, lambda i, j: sp.expand(sp.trace(_kron(i, j) * unshuffled))
    )


# ---------------------------------------------------------------------------
# Table 1 templates: scaled covariance blocks alpha1*H1S as functions of the
# SCALED parameters. Parameter order per type: (x, w) where x is the real
# diagonal-type parameter (alpha1*P / alpha1*K / alpha1*E) and w the complex
# off-parameter (alpha1*W / alpha1*N / alpha1*V). The dependent parameter
# (alpha1*Pbar etc.) follows from the rank-1 relation:  xbar = w*conj(w)/x.
# ---------------------------------------------------------------------------

def _type1(x, w, primary="outer"):
    """Type 1: H = [[P,0,0,W],[0,0,0,0],[0,0,0,0],[W*,0,0,Pbar]].

    `primary` selects which real parameter `x` stands for: "outer" -> P
    (top-left), "center" -> Pbar (bottom-right); the other follows from
    the rank-1 relation P*Pbar = W*conj(W).
    """
    xbar = w * sp.conjugate(w) / x
    p, pbar = (x, xbar) if primary == "outer" else (xbar, x)
    z = sp.Integer(0)
    return sp.Matrix([
        [p, z, z, w],
        [z, z, z, z],
        [z, z, z, z],
        [sp.conjugate(w), z, z, pbar],
    ])


def _type2(x, w, primary="outer"):
    """Type 2: corners K, edges N; center Kbar (Table 1, row 2)."""
    xbar = w * sp.conjugate(w) / x
    k, kbar = (x, xbar) if primary == "outer" else (xbar, x)
    cw = sp.conjugate(w)
    return sp.Matrix([
        [k, w, w, k],
        [cw, kbar, kbar, cw],
        [cw, kbar, kbar, cw],
        [k, w, w, k],
    ])


def _type3(x, w, primary="outer"):
    """Type 3: corners E, edges +/-V; center +/-Ebar (Table 1, row 3)."""
    xbar = w * sp.conjugate(w) / x
    e, ebar = (x, xbar) if primary == "outer" else (xbar, x)
    cw = sp.conjugate(w)
    return sp.Matrix([
        [e, w, -w, e],
        [cw, ebar, -ebar, cw],
        [-cw, -ebar, ebar, -cw],
        [e, w, -w, e],
    ])


TYPE1, TYPE2, TYPE3 = "type1", "type2", "type3"

#: type -> (scaled template builder, alpha1-from-(x, w) formula).
#: The alpha1 formula is symmetric in (primary, dependent) since
#: x * xbar = w * conj(w): trace works out identically for both variants.
SYMMETRY_TEMPLATES = {
    TYPE1: (_type1, lambda x, w: x + w * sp.conjugate(w) / x),
    TYPE2: (_type2, lambda x, w: 2 * (x + w * sp.conjugate(w) / x)),
    TYPE3: (_type3, lambda x, w: 2 * (x + w * sp.conjugate(w) / x)),
}
