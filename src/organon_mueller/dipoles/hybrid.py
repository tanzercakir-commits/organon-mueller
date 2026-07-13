"""Hybridization: normal modes, hybrid basis, coefficient extraction
(PRB 98, 045410 Secs. IV.B, V)."""
from __future__ import annotations

import sympy as sp

from .dimer import coupling_lambda, interaction_jones, jones_projector, \
    jones_to_hvector

__all__ = [
    "coupled_system_matrix",
    "lorentzian",
    "hybrid_frequencies",
    "hybrid_basis",
    "decomposition_coefficients",
]


def coupled_system_matrix(phi1, phi2, lam1, lam2, delta1, delta2) -> sp.Matrix:
    """The 4x4 A of Eq. (41) (lam_i = 1/alpha_i). Its determinant equals
    lam1*lam2*(lam1*lam2 - Lambda^2) — proven symbolically in tests; the
    nonzero normal modes are lam1*lam2 = Lambda^2 (Eq. 43)."""
    c1, s1 = sp.cos(phi1), sp.sin(phi1)
    c2, s2 = sp.cos(phi2), sp.sin(phi2)
    a1, b1, cc1 = c1 * c1, c1 * s1, s1 * s1
    a2, b2, cc2 = c2 * c2, c2 * s2, s2 * s2
    return sp.Matrix([
        [lam1, 0, -delta1 * a1, -delta2 * b1],
        [0, lam1, -delta1 * b1, -delta2 * cc1],
        [-delta1 * a2, -delta2 * b2, lam2, 0],
        [-delta1 * b2, -delta2 * cc2, 0, lam2],
    ])


def lorentzian(omega, omega0, eta, damping=0) -> sp.Expr:
    """alpha(omega) = eta*omega0 ... (Eq. 39). NOTE the paper's printed
    numerator is eta_i omega_i; the hybridization algebra of Eqs. (44)-(46)
    is consistent with eta_i omega_i^2 (lam = (omega_i^2-omega^2)/(eta_i
    omega_i^2) in Eq. 44). We implement the Eq.-44-consistent form and
    anchor the derived frequencies, not the profile itself."""
    return eta * omega0 ** 2 / (omega0 ** 2 - omega ** 2
                                - sp.I * damping * omega)


def hybrid_frequencies(omega1, omega2, eta1, eta2, lam_coupling):
    """DERIVE omega_pm from lam1*lam2 = Lambda^2 (Eq. 43) with undamped
    Lorentzians: quadratic in omega^2, solved exactly (anchored against
    the paper's Eq. 45 in tests).

    Strong-coupling note (review defect 3a): for eta1*eta2*Lambda^2 > 1
    the lower root omega_-^2 goes negative (imaginary "frequency" — the
    undamped model leaves its validity range); numeric inputs in that
    regime raise instead of silently returning an imaginary value (K26).
    """
    w = sp.symbols("omega_h", positive=True)
    lam1 = (omega1 ** 2 - w ** 2) / (eta1 * omega1 ** 2)
    lam2 = (omega2 ** 2 - w ** 2) / (eta2 * omega2 ** 2)
    sols = sp.solve(sp.expand(lam1 * lam2 - lam_coupling ** 2), w ** 2)
    if len(sols) == 1:  # double root (Lambda == 0, omega1 == omega2)
        sols = [sols[0], sols[0]]
    if len(sols) != 2:
        raise ValueError(f"expected 2 roots in omega^2, got {len(sols)}")
    for s in sols:
        if s.is_number and complex(s).real < 0:
            raise ValueError(
                f"omega^2 root {s} < 0: strong coupling "
                "(eta1*eta2*Lambda^2 > 1) is outside the undamped model")
    return tuple(sp.sqrt(sp.simplify(s)) for s in sols)


def hybrid_basis(phi1, phi2, g1=None, g2=None):
    """|h_pm> (Eq. 63; geometric Eq. 64 when g1 == g2 or omitted)."""
    h1 = jones_to_hvector(jones_projector(phi1)).to_column()
    h2 = jones_to_hvector(jones_projector(phi2)).to_column()
    hint = jones_to_hvector(interaction_jones(phi1, phi2)).to_column()
    if g1 is None and g2 is None:
        mid = (h1 + h2) / 2
    else:
        prod = sp.sympify(g1) * sp.sympify(g2)
        if prod.is_number and abs(complex(prod)) < 1e-300:
            raise ValueError("g1*g2 == 0: hybrid basis undefined (division "
                             "by sqrt(g1 g2))")
        mid = (g1 * h1 + g2 * h2) / (2 * sp.sqrt(g1 * g2))
    return mid + hint / 2, mid - hint / 2


def decomposition_coefficients(t_vector: sp.Matrix, phi1, phi2,
                               simplify: bool = True):
    """Solve |t> = g1|h1> + g2|h2> + gint|hint> for (g1, g2, gint) —
    the general-angle version of the paper's Eq. (70) inversion.

    Guards (K26): (i) the 3x3 system is singular exactly when phi1 ==
    phi2 mod pi (basis det = sin^3(phi1-phi2)/2 — reviewer-derived); a
    ValueError with the reason is raised. (ii) The 4th component of the
    geometric basis vectors is identically zero (paper: "the fourth
    equation is trivial"), so a NUMERIC t with t[3] != 0 (dephased /
    chiral data) is OUTSIDE the span and is rejected instead of silently
    projected (review defect 2). For symbolic t the caller owns this
    precondition."""
    t3 = sp.simplify(sp.Matrix(t_vector)[3, 0])
    if t3.is_number and abs(complex(t3)) > 1e-12:
        raise ValueError(
            f"t[3] = {t3} != 0: the geometric basis spans only h4 == 0 "
            "vectors; dephased/chiral data cannot be decomposed here "
            "without silent information loss (K26)")
    h1 = jones_to_hvector(jones_projector(phi1)).to_column()
    h2 = jones_to_hvector(jones_projector(phi2)).to_column()
    hint = jones_to_hvector(interaction_jones(phi1, phi2)).to_column()
    basis = sp.Matrix.hstack(h1[:3, 0], h2[:3, 0], hint[:3, 0])
    det = sp.simplify(basis.det())
    near_zero = det.is_number and abs(complex(det)) < 1e-12
    if det == 0 or near_zero:
        raise ValueError(
            "decomposition basis is singular (parallel dipoles phi1 == phi2 "
            "mod pi make J1, J2, Jint linearly dependent)")
    sol = basis.LUsolve(sp.Matrix(t_vector[:3, 0]))
    if simplify:
        sol = sp.simplify(sol)
    return sol[0], sol[1], sol[2]
