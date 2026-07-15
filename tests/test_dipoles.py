"""Stage-12: coupled-dipole engine vs PRB 98, 045410 (K28/K33 anchors).

Print-factor notes (M30): Eq. 33 and Eq. 37 report h-vectors up to an
overall scale relative to the paper's own half-convention (Eq. 29);
anchors below carry the explicit factors. Eq. 39's printed numerator
(eta*omega) is inconsistent with the paper's own Eq. 44 (eta*omega^2);
we implement the Eq.-44-consistent profile and anchor Eq. 45."""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.algebra.states import HVector
from organon_mueller.dipoles import (
    coupled_system_matrix,
    lorentzian,
    coupling_lambda,
    decomposition_coefficients,
    dephased_interaction_jones,
    hybrid_basis,
    hybrid_frequencies,
    interaction_jones,
    jones_projector,
    jones_to_hvector,
    scattering_matrix_decomposed,
    scattering_matrix_direct,
    scattering_matrix_numeric,
)

PHI1, PHI2 = sp.symbols("phi1 phi2", real=True)
A1, A2 = sp.symbols("alpha1 alpha2", complex=True)
D1, D2 = sp.symbols("delta1 delta2", complex=True)


# -- the central anchor theorem (Eq. 25) -----------------------------------------

def test_decomposition_theorem_symbolic():
    """DERIVED T (4x4 coupled solve) == paper's three-term form, exactly,
    for fully symbolic angles and parameters."""
    direct = scattering_matrix_direct(PHI1, PHI2, A1, A2, D1, D2)
    dec = scattering_matrix_decomposed(PHI1, PHI2, A1, A2, D1, D2)
    diff = (direct - dec).applyfunc(
        lambda e: sp.simplify(sp.expand_trig(sp.together(e))))
    assert diff == sp.zeros(2, 2)


def test_decomposition_numeric_seeded():
    rng = np.random.default_rng(20260713)
    for _ in range(4):
        phi1, phi2 = rng.uniform(0, 2 * np.pi, 2)
        a1, a2, d1, d2 = (complex(x, y) * 0.3 for x, y in
                          rng.standard_normal((4, 2)))
        num = scattering_matrix_numeric(phi1, phi2, a1, a2, d1, d2)
        sym = scattering_matrix_decomposed(
            sp.Float(phi1), sp.Float(phi2), a1, a2, d1, d2)
        sym = np.array(sp.matrix2numpy(sym.evalf(), dtype=complex))
        assert np.max(np.abs(num - sym)) < 1e-10


def test_closed_forms_eqs_14_17_symbolic():
    """Paper Eqs. (14)-(17): p_i closed forms — symbolic anchor (added
    stage-15 review: the ADDENDUM claims 'symbolically', so a permanent
    symbolic test must exist, not just the archived numeric probe)."""
    e0x, e0y = sp.symbols("e0x e0y", complex=True)
    lam = coupling_lambda(PHI1, PHI2, D1, D2)
    e1_ = sp.cos(PHI1) * e0x + sp.sin(PHI1) * e0y
    e2_ = sp.cos(PHI2) * e0x + sp.sin(PHI2) * e0y
    den = 1 - A1 * A2 * lam ** 2
    p1 = A1 * sp.Matrix([sp.cos(PHI1), sp.sin(PHI1)]) * (e1_ + A2 * lam * e2_) / den
    p2 = A2 * sp.Matrix([sp.cos(PHI2), sp.sin(PHI2)]) * (e2_ + A1 * lam * e1_) / den
    t = scattering_matrix_decomposed(PHI1, PHI2, A1, A2, D1, D2)
    diff = (t * sp.Matrix([e0x, e0y]) - (p1 + p2)).applyfunc(
        lambda e: sp.simplify(sp.expand_trig(sp.together(e))))
    assert diff == sp.zeros(2, 1)


# -- normal modes (Eqs. 41-46) ----------------------------------------------------

def test_determinant_structure_theorem():
    lam1, lam2 = sp.symbols("lam1 lam2", complex=True)
    amat = coupled_system_matrix(PHI1, PHI2, lam1, lam2, D1, D2)
    lam = coupling_lambda(PHI1, PHI2, D1, D2)
    assert sp.simplify(amat.det() - lam1 * lam2 * (lam1 * lam2 - lam ** 2)) == 0


def test_hybrid_frequencies_match_eq45():
    w1, w2, e1, e2, lc = sp.symbols("w1 w2 eta1 eta2 Lam", positive=True)
    got = hybrid_frequencies(w1, w2, e1, e2, lc)
    disc = sp.sqrt((w1 ** 2 - w2 ** 2) ** 2 + 4 * w1 ** 2 * w2 ** 2 * e1 * e2 * lc ** 2)
    paper = {sp.sqrt((w1 ** 2 + w2 ** 2 + s * disc) / 2) for s in (1, -1)}
    got2 = {sp.expand(sp.simplify(g ** 2)) for g in got}
    paper2 = {sp.expand(sp.simplify(p ** 2)) for p in paper}
    # same root set: compare the symmetric functions (sum and product)
    assert sp.simplify(sum(got2) - sum(paper2)) == 0
    assert sp.simplify(sp.prod(got2) - sp.prod(paper2)) == 0


def test_identical_dipoles_eq46():
    w0, eta, lc = sp.symbols("w0 eta Lam", positive=True)
    got = hybrid_frequencies(w0, w0, eta, eta, lc)
    paper = {w0 ** 2 * (1 + eta * lc), w0 ** 2 * (1 - eta * lc)}
    assert ({sp.expand(sp.simplify(g ** 2)) for g in got}
            == {sp.expand(p) for p in paper})


# -- covariance-vector anchors (Eqs. 29, 31-33, 37) --------------------------------

def test_h_vector_convention_sentinel():
    """Paper Eq. 29 == our JOSA A HVector convention, both directions."""
    hv = HVector.generic("s")
    back = jones_to_hvector(hv.to_jones())
    assert all(sp.simplify(a - b) == 0 for a, b in
               zip(back.to_column(), hv.to_column()))


def test_single_dipole_h_vector_eq31():
    h = jones_to_hvector(jones_projector(PHI1)).to_column()
    paper = sp.Matrix([1, sp.cos(2 * PHI1), sp.sin(2 * PHI1), 0]) / 2
    assert sp.simplify(h - paper) == sp.zeros(4, 1)


def test_interaction_h_vector_eq32():
    h = jones_to_hvector(interaction_jones(PHI1, PHI2)).to_column()
    paper = sp.Matrix([sp.cos(PHI1 - PHI2), sp.cos(PHI1 + PHI2),
                       sp.sin(PHI1 + PHI2), 0])
    assert sp.simplify(h - paper) == sp.zeros(4, 1)


def test_serial_product_chirality_eq33():
    """Serial J2*J1: 4th component (i/4)sin(2(phi1-phi2)) — nonzero
    UNLESS parallel (dphi = 0 mod pi) OR crossed (dphi = pi/2, where the
    projector product annihilates entirely). Paper's Eq. 33 vector holds
    up to the overall factor cos(dphi)/2 (M30 print-scale note)."""
    h = jones_to_hvector(jones_projector(PHI2) * jones_projector(PHI1))
    factor = sp.cos(PHI1 - PHI2) / 2
    paper = sp.Matrix([sp.cos(PHI1 - PHI2), sp.cos(PHI1 + PHI2),
                       sp.sin(PHI1 + PHI2),
                       sp.I * sp.sin(PHI1 - PHI2)]) * factor
    assert sp.simplify(h.to_column() - paper) == sp.zeros(4, 1)


def test_dephased_interaction_optical_activity_eq37():
    """gamma-component of J'_int: -(i/2) sin(phi1-phi2)(1 - e^{i chi})
    (half-convention; the paper's Eq. 37 prints 2x — M30). Zero iff
    chi = 0 or parallel dipoles; PURELY circular at chi = pi."""
    chi = sp.symbols("chi", real=True)
    h = jones_to_hvector(dephased_interaction_jones(PHI1, PHI2, chi))
    expected = -sp.I * sp.sin(PHI1 - PHI2) * (1 - sp.exp(sp.I * chi)) / 2
    assert sp.simplify(h.gamma - expected) == 0
    assert sp.simplify(h.gamma.subs(chi, 0)) == 0
    assert sp.simplify(h.gamma.subs(PHI2, PHI1)) == 0
    at_pi = [sp.simplify(c.subs(chi, sp.pi)) for c in h.to_column()]
    assert at_pi[0] == 0 and at_pi[1] == 0 and at_pi[2] == 0
    assert sp.simplify(at_pi[3] + sp.I * sp.sin(PHI1 - PHI2)) == 0


# -- special cases and sentinels ----------------------------------------------------

def test_parallel_perpendicular_cases_eq53_54():
    t = scattering_matrix_decomposed(0, 0, A1, A2, D1, D2)
    paper = (A1 + A2 + 2 * A1 * A2 * D1) / (1 - A1 * A2 * D1 ** 2)
    assert sp.simplify(t - paper * sp.Matrix([[1, 0], [0, 0]])) == sp.zeros(2, 2)
    t = scattering_matrix_decomposed(sp.pi / 2, sp.pi / 2, A1, A2, D1, D2)
    paper = (A1 + A2 + 2 * A1 * A2 * D2) / (1 - A1 * A2 * D2 ** 2)
    assert sp.simplify(t - paper * sp.Matrix([[0, 0], [0, 1]])) == sp.zeros(2, 2)


def test_lambda_sentinels():
    """(0, 90): orthogonal + axis-aligned -> Lambda = 0 (no hybridization,
    Fig. 3c). (-45, 45): orthogonal but tilted -> Lambda != 0 (Fig. 3f)."""
    assert sp.simplify(coupling_lambda(0, sp.pi / 2, D1, D2)) == 0
    lam = sp.simplify(coupling_lambda(-sp.pi / 4, sp.pi / 4, D1, D2))
    assert sp.simplify(lam - (D1 - D2) / 2) == 0 and lam != 0


# -- hybrid basis (Eqs. 61-64, 69-71) -------------------------------------------------

def test_hybrid_identity_theorem():
    """|t> = nu+|h+> + nu-|h-> for GENERIC g1, g2, gint and angles."""
    g1, g2, gint = sp.symbols("g1 g2 gint", complex=True)
    hp, hm = hybrid_basis(PHI1, PHI2, g1, g2)
    nup = sp.sqrt(g1 * g2) + gint
    num = sp.sqrt(g1 * g2) - gint
    h1 = jones_to_hvector(jones_projector(PHI1)).to_column()
    h2 = jones_to_hvector(jones_projector(PHI2)).to_column()
    hint = jones_to_hvector(interaction_jones(PHI1, PHI2)).to_column()
    t = g1 * h1 + g2 * h2 + gint * hint
    assert sp.simplify(nup * hp + num * hm - t) == sp.zeros(4, 1)


def test_geometric_basis_orthogonality_theorem():
    """g1 = g2 -> <h+|h-> = 0 for ALL angles (paper states it; here a
    symbolic theorem via |h1+h2|^2 == |hint|^2 == 1 + cos^2(dphi))."""
    hp, hm = hybrid_basis(PHI1, PHI2)
    inner = sum(sp.conjugate(a) * b for a, b in zip(hp, hm))
    assert sp.simplify(sp.expand_complex(sp.expand(inner))) == 0


def test_coefficient_inversion_matches_eq70():
    h0, h1v, h2v = sp.symbols("h0 h1 h2", complex=True)
    t = sp.Matrix([h0, h1v, h2v, 0])
    g1, g2, gint = decomposition_coefficients(t, sp.pi / 2, 3 * sp.pi / 4)
    assert sp.simplify(g1 - 2 * (h0 + h2v)) == 0
    assert sp.simplify(g2 - 2 * (h0 + h1v)) == 0
    assert sp.simplify(gint + sp.sqrt(2) * (h0 + h1v + h2v)) == 0


def test_coefficient_roundtrip_general_angles():
    g1t, g2t, gintt = 0.3 + 0.1j, -0.2 + 0.4j, 0.05 - 0.3j
    phi1, phi2 = 0.4, 1.3
    h1 = jones_to_hvector(jones_projector(phi1)).to_column()
    h2 = jones_to_hvector(jones_projector(phi2)).to_column()
    hint = jones_to_hvector(interaction_jones(phi1, phi2)).to_column()
    t = (g1t * h1 + g2t * h2 + gintt * hint).evalf()
    g1, g2, gint = decomposition_coefficients(t, phi1, phi2)
    for got, true in ((g1, g1t), (g2, g2t), (gint, gintt)):
        assert abs(complex(got) - true) < 1e-10


def test_intensity_splits_across_hybrid_modes():
    """I = I+ + I- when g1 == g2 (paper Eq. 74; orthogonal basis)."""
    g, gint = 0.4 - 0.2j, 0.15 + 0.3j
    phi1, phi2 = 0.5, 1.4
    hp, hm = hybrid_basis(phi1, phi2)
    h1 = jones_to_hvector(jones_projector(phi1)).to_column()
    h2 = jones_to_hvector(jones_projector(phi2)).to_column()
    hint = jones_to_hvector(interaction_jones(phi1, phi2)).to_column()
    t = (g * h1 + g * h2 + gint * hint).evalf()
    nup, num = g + gint, g - gint  # sqrt(g*g) = g up to branch; |.|^2 safe
    inner = lambda a, b: complex(  # noqa: E731
        sum(sp.conjugate(x) * y for x, y in zip(a, b)).evalf())
    total = inner(t, t).real
    split = (abs(nup) ** 2 * inner(hp, hp).real
             + abs(num) ** 2 * inner(hm, hm).real)
    assert abs(total - split) < 1e-10


def test_lorentzian_consistent_with_eq44():
    """1/lorentzian == (w0^2 - w^2)/(eta w0^2) at zero damping — ties the
    implemented profile to the Eq-44 form used by hybrid_frequencies
    (M30(b) resolution anchored)."""
    w, w0, eta = sp.symbols("w w0 eta", positive=True)
    lam = sp.simplify(1 / lorentzian(w, w0, eta))
    assert sp.simplify(lam - (w0 ** 2 - w ** 2) / (eta * w0 ** 2)) == 0


def test_strong_coupling_and_double_root_guards():
    with pytest.raises(ValueError, match="strong coupling"):
        hybrid_frequencies(1.0, 1.0, 2.0, 2.0, 1.0)
    wp, wm = hybrid_frequencies(1.5, 1.5, 0.3, 0.3, 0)  # double root
    assert sp.simplify(wp - wm) == 0 and sp.simplify(wp - 1.5) == 0


def test_t3_span_guard():
    """Numeric t with t[3] != 0 must be rejected (review defect 2)."""
    t = sp.Matrix([0.3, 0.1, 0.2, 0.05 + 0.02j])
    with pytest.raises(ValueError, match="h4"):
        decomposition_coefficients(t, 0.4, 1.3)


# -- guards (K26) ----------------------------------------------------------------------

def test_singular_basis_guard():
    with pytest.raises(ValueError, match="singular"):
        decomposition_coefficients(sp.Matrix([1, 0, 0, 0]), 0.7, 0.7)


def test_resonance_guard():
    # arrange alpha1*alpha2*Lambda^2 == 1 exactly (phi=0 -> Lambda=delta1)
    with pytest.raises(ValueError, match="resonance"):
        scattering_matrix_numeric(0.0, 0.0, 2.0, 2.0, 0.5, 0.1)


def test_non_finite_guard():
    with pytest.raises(ValueError, match="finite"):
        scattering_matrix_numeric(0.0, 1.0, np.nan, 1.0, 0.1, 0.1)
