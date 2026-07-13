"""Stage-14: 3D dimer + ensemble OA vs the OA-in-ensemble preprint
(K28/K33 anchors; M30 #5/#6 print notes probe-verified)."""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.dipoles.ensemble import (
    backscatter_jones_3d,
    coupling_delta_3d,
    ensemble_covariance,
    ensemble_gamma,
    forward_jones_3d,
    gamma_paper,
    is_chiral,
    jones_3d_numeric,
    solve_dimer_3d,
    transverse_jones_3d,
)

M = sp.symbols("mx my mz", real=True)
N = sp.symbols("nx ny nz", real=True)
RZ, RX = sp.symbols("rz rx", real=True)
AL, DL = sp.symbols("al_e dl_e", complex=True)
MU = sp.Symbol("mu_e")


def _mu():
    return AL / (1 - (AL * DL) ** 2)  # eps = 1


def _simp(e):
    # rewrite trig to exp first: the derived side is in exp form
    return sp.simplify(sp.expand(sp.together(e.rewrite(sp.exp))))


# -- anchors -----------------------------------------------------------------------

def test_solve_matches_eqs_21_24():
    ex, ey = sp.symbols("Ex Ey", complex=True)
    qn, qm = solve_dimer_3d(M, N, RZ, AL, DL, ex, ey)
    mu = _mu()
    em_, ep_ = sp.exp(-sp.I * RZ / 2), sp.exp(sp.I * RZ / 2)
    pnx_paper = mu * N[0] * ((em_ * N[0] + ep_ * M[0] * AL * DL) * ex
                             + (em_ * N[1] + ep_ * M[1] * AL * DL) * ey)
    pmy_paper = mu * M[1] * ((ep_ * M[0] + em_ * N[0] * AL * DL) * ex
                             + (ep_ * M[1] + em_ * N[1] * AL * DL) * ey)
    assert _simp(qn * N[0] - pnx_paper) == 0   # Eq. 21
    assert _simp(qm * M[1] - pmy_paper) == 0   # Eq. 24


def test_forward_jones_matches_eqs_26_29():
    j = forward_jones_3d(M, N, RZ, AL, DL)
    mu, ad = _mu(), AL * DL
    paper = mu * sp.Matrix([
        [N[0] ** 2 + M[0] ** 2 + 2 * N[0] * M[0] * sp.cos(RZ) * ad,
         N[0] * N[1] + M[0] * M[1] + N[0] * M[1] * sp.exp(sp.I * RZ) * ad
         + M[0] * N[1] * sp.exp(-sp.I * RZ) * ad],
        [N[0] * N[1] + M[0] * M[1] + N[0] * M[1] * sp.exp(-sp.I * RZ) * ad
         + M[0] * N[1] * sp.exp(sp.I * RZ) * ad,
         N[1] ** 2 + M[1] ** 2 + 2 * N[1] * M[1] * sp.cos(RZ) * ad],
    ])
    assert (j - paper).applyfunc(_simp) == sp.zeros(2, 2)


def test_gamma_z_eq31_with_labeling_note():
    """gamma_z = -2 mu alpha delta (n x m)_z sin(k rz). The PAPER prints
    the cross product as (m x n)_z — probe showed the consistent label
    is (n x m)_z = nx*my - ny*mx (M30 #5); magnitude/physics unaffected
    (sign flips with the m/n naming)."""
    g = gamma_paper(forward_jones_3d(M, N, RZ, AL, DL))
    nxm_z = N[0] * M[1] - N[1] * M[0]
    assert _simp(g + 2 * _mu() * AL * DL * nxm_z * sp.sin(RZ)) == 0


def test_gamma_x_eq33_and_split():
    j = transverse_jones_3d(M, N, RZ, RX, AL, DL)
    g = gamma_paper(j)
    mu, ad = _mu(), AL * DL
    g1 = -sp.I * mu * (N[1] * (N[0] + N[2]) * sp.exp(-sp.I * (RZ - RX) / 2)
                       + M[1] * (M[0] + M[2]) * sp.exp(sp.I * (RZ - RX) / 2))
    g2 = -sp.I * mu * ad * (
        (N[2] * M[1] + N[1] * M[0]) * sp.exp(sp.I * (RZ + RX) / 2)
        + (M[2] * N[1] + M[1] * N[0]) * sp.exp(-sp.I * (RZ + RX) / 2))
    assert _simp(g - (g1 + g2)) == 0          # Eq. 33 = 34 + 35
    # "coupling-independent" (paper): the gamma_x1 BRACKET is delta-free
    # (the common mu prefactor does contain delta, but gamma_x1 SURVIVES
    # the uncoupled limit while gamma_x2 dies):
    assert sp.simplify(g2.subs(DL, 0)) == 0
    assert sp.simplify(g1.subs(DL, 0)) != 0
    assert not sp.simplify(g1 * (1 - (AL * DL) ** 2) / AL).has(DL)


def test_gamma_backscatter_corrected_eq9():
    """Eq. 9's bracket is right but the printed prefactor -2i*eps*alpha*mu
    double-counts eps*alpha (mu = eps*alpha/(1-(ad)^2)); the derived
    prefactor is -2i*mu (M30 #6, probe-verified)."""
    g = gamma_paper(backscatter_jones_3d(M, N, RZ, AL, DL))
    core = (N[0] * N[1] * sp.exp(-sp.I * RZ) + M[0] * M[1] * sp.exp(sp.I * RZ)
            + (N[0] * M[1] + M[0] * N[1]) * AL * DL)
    assert _simp(g + 2 * sp.I * _mu() * core) == 0


def test_uncoupled_gamma_z_vanishes_theorem():
    """delta = 0 => gamma_z == 0 for EVERY orientation (paper's central
    forward-scattering claim), symbolically."""
    g = gamma_paper(forward_jones_3d(M, N, RZ, AL, 0))
    assert _simp(g) == 0


def test_coupling_delta_and_chirality():
    u = sp.symbols("ux uy uz", real=True)
    d = coupling_delta_3d(M, N, u, sp.Symbol("Ae"), sp.Symbol("Be"))
    assert d.has(sp.Symbol("Ae")) and d.has(sp.Symbol("Be"))
    assert is_chiral([1, 0, 0], [0, 1, 0], [0, 0, 1])       # m x n || r
    assert not is_chiral([1, 0, 0], [0, 1, 0], [1, 1, 0])   # coplanar


# -- ensemble claims (deterministic, CI-fast) ----------------------------------------

def test_ensemble_claims_forward():
    chiral = ensemble_gamma(chiral=True, n_samples=800)
    achiral = ensemble_gamma(chiral=False, n_samples=800)
    uncoupled = ensemble_gamma(chiral=True, n_samples=100,
                               a_coef=0.0, b_coef=0.0)
    # margins widened per review (alt-seed stats: ratio >= 4.67,
    # residual <= 0.110): numpy Generator streams carry no cross-version
    # stability guarantee, so the thresholds must not be marginal
    assert abs(chiral["mean_gamma"]) > 3 * abs(achiral["mean_gamma"])
    # achiral: mean ~ 0 but mean |gamma| stays finite (nonideal-ensemble OA)
    assert abs(achiral["mean_gamma"]) < 0.2 * achiral["mean_abs_gamma"]
    # uncoupled: gamma_z == 0 pointwise
    assert uncoupled["mean_abs_gamma"] < 1e-14


def test_ensemble_deterministic():
    a = ensemble_gamma(n_samples=50)
    b = ensemble_gamma(n_samples=50)
    assert a == b


# -- depolarization bridge (first end-to-end) -----------------------------------------

def test_bridge_two_orientation_mixture():
    """A 2-orientation ensemble covariance is rank <= 2, PSD, trace-1,
    and flows into the decomposition layer with REASONED outcomes (K21)."""
    from organon_mueller.decomposition.rank3 import propose_decompositions

    rng = np.random.default_rng(20260713)

    def orient():
        u = rng.standard_normal(3)
        u /= np.linalg.norm(u)
        v = rng.standard_normal(3)
        v -= u * (u @ v)
        v /= np.linalg.norm(v)
        z = np.cross(u, v)
        return (u + v) / np.sqrt(2), (u - v) / np.sqrt(2), z

    cov = ensemble_covariance([orient(), orient()])
    eig = np.linalg.eigvalsh(cov)
    assert abs(np.trace(cov).real - 1) < 1e-12
    assert eig.min() > -1e-10
    assert int(np.sum(eig > 1e-9 * eig.max())) <= 2
    report = propose_decompositions(cov)
    labels = {lb for lb, _ in report.successes} | {lb for lb, _ in report.failures}
    assert labels                       # every hypothesis attempted...
    assert all(r for _, r in report.failures)  # ...and failures reasoned


def test_numeric_guards():
    with pytest.raises(ValueError, match="finite"):
        jones_3d_numeric([np.nan, 0, 0], [0, 1, 0], [0, 0, 1], 0.3, 0.1, 0.1)
    with pytest.raises(ValueError, match="coincident"):
        jones_3d_numeric([1, 0, 0], [0, 1, 0], [0, 0, 0], 0.3, 0.1, 0.1)
    # resonance: n.m = 0, (n.u)(m.u) = 1/2 * ... craft alpha*delta = 1
    m, n = [1, 0, 0], [0, 1, 0]
    r = np.array([1.0, 1.0, 0]) / np.sqrt(2)
    # delta = (n.u)(m.u)*B = 0.5*B ; pick B so alpha*delta = 1
    with pytest.raises(ValueError, match="resonance"):
        jones_3d_numeric(m, n, r, 2.0, 0.0, 1.0)
