"""Stage-13: general-geometry dimer + reciprocity vs Symmetry 12, 1790
(2020) — K28/K33 anchors and the Perrin theorem."""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.dipoles.dimer import (
    jones_to_hvector,
    scattering_matrix_decomposed,
)
from organon_mueller.dipoles.general import (
    case_A_jones,
    case_B_jones,
    forward_gamma_general,
    forward_jones_general,
    forward_jones_numeric,
    reciprocity_transform,
    symmetry_deltas,
)

TH, F1, F2 = sp.symbols("theta_g phi1_g phi2_g", real=True)
A1, A2 = sp.symbols("alphag1 alphag2", complex=True)
AC, BC = sp.symbols("Ag Bg", complex=True)
E1S, E2S = sp.symbols("e1g e2g", complex=True)
ALL = (TH, F1, F2, A1, A2, AC, BC, E1S, E2S)


def _paper_a11():
    """Eq. (A11), entered FULLY by hand as the anchor (K28/K33; review:
    deltas inlined so the anchor shares no geometry encoding with the
    module — symmetry_deltas is tested against these separately)."""
    s1, c1, c2 = sp.sin(F1), sp.cos(F1), sp.cos(F2)
    d1s = AC + s1 ** 2 * BC
    d2s = c1 * c2 * s1 * BC
    a_, b_, c_ = (sp.cos(TH) ** 2, sp.cos(TH) * sp.sin(TH), sp.sin(TH) ** 2)
    dd1, dd2 = b_ * d1s + a_ * d2s, c_ * d1s + b_ * d2s
    n = 1 - E1S ** 2 * A1 * A2 * (2 * b_ * d1s * d2s + c_ * d1s ** 2
                                  + a_ * d2s ** 2)
    j1 = sp.Matrix([[0, 0], [0, 1]])
    j2 = sp.Matrix([[a_, b_], [b_, c_]])
    jint = sp.Matrix([[0, dd1], [E2S ** 2 * dd1, (1 + E2S ** 2) * dd2]])
    return (E2S * A1 * j1 + E2S * A2 * j2 + E1S * A1 * A2 * jint) / n, n, dd1


def test_symmetry_deltas_match_hand_values():
    """Module's delta encoding == the hand-typed paper values (kept as a
    separate check now that _paper_a11 is fully module-independent)."""
    d1s, d2s, dd1, dd2 = symmetry_deltas(TH, F1, F2, AC, BC)
    s1, c1, c2 = sp.sin(F1), sp.cos(F1), sp.cos(F2)
    a_, b_, c_ = (sp.cos(TH) ** 2, sp.cos(TH) * sp.sin(TH), sp.sin(TH) ** 2)
    assert sp.simplify(d1s - (AC + s1 ** 2 * BC)) == 0
    assert sp.simplify(d2s - c1 * c2 * s1 * BC) == 0
    assert sp.simplify(dd1 - (b_ * d1s + a_ * d2s)) == 0
    assert sp.simplify(dd2 - (c_ * d1s + b_ * d2s)) == 0


def test_forward_jones_matches_eq_a11():
    """Central anchor: DERIVED T (scalar-reduced coupled solve, probe-
    resolved e2*p1 + p2 bookkeeping) == paper Eq. (A11), symbolically."""
    derived = forward_jones_general(TH, F1, F2, A1, A2, AC, BC, E1S, E2S)
    paper, _, _ = _paper_a11()
    diff = (derived - paper).applyfunc(
        lambda e: sp.simplify(sp.expand_trig(sp.together(e))))
    assert diff == sp.zeros(2, 2)


def test_special_case_eq_a12():
    """phi1 = -45deg, theta = phi2 = 0, e2 = 1: J = g[[1, e1 a d],
    [e1 a d, 1]], d = -B/2 (paper Eqs. 3-4/A12)."""
    al = sp.symbols("al_s", complex=True)
    j = forward_jones_general(0, -sp.pi / 4, 0, al, al, AC, BC, E1S, 1)
    delta = -BC / 2
    g = al / (1 - E1S ** 2 * al ** 2 * delta ** 2)
    paper = g * sp.Matrix([[1, E1S * al * delta], [E1S * al * delta, 1]])
    diff = (j - paper).applyfunc(lambda e: sp.simplify(sp.together(e)))
    assert diff == sp.zeros(2, 2)


def test_prb_consistency_sentinel():
    """M36: with e1 = e2 = 1, theta free, phi1 = -pi/2 (u = (0,-1,0) —
    the PRB Fig-1 geometry, dimer axis y) the general solver must equal
    the PRB decomposition with dipole 1 vertical (phi = pi/2), dipole 2
    at theta, delta1 = A, delta2 = A + B."""
    j_gen = forward_jones_general(TH, -sp.pi / 2, 0, A1, A2, AC, BC, 1, 1)
    j_prb = scattering_matrix_decomposed(sp.pi / 2, TH, A1, A2, AC, AC + BC)
    diff = (j_gen - j_prb).applyfunc(
        lambda e: sp.simplify(sp.expand_trig(sp.together(e))))
    assert diff == sp.zeros(2, 2)


# -- reciprocity ---------------------------------------------------------------

def test_reciprocity_transform_pattern_and_involution():
    j = sp.Matrix(2, 2, sp.symbols("j00 j01 j10 j11", complex=True))
    r = reciprocity_transform(j)
    assert r == sp.Matrix([[j[0, 0], -j[1, 0]], [-j[0, 1], j[1, 1]]])
    assert reciprocity_transform(r) == j


def test_case_a_b_anchors_and_reciprocity_theorem():
    al = sp.symbols("al_s", complex=True)
    delta = -BC / 2
    mu = E1S * al * delta
    g = al / (1 - E1S ** 2 * al ** 2 * delta ** 2)
    ja = case_A_jones(al, BC, E1S)
    jb = case_B_jones(al, BC, E1S)
    assert sp.simplify(ja - g * sp.Matrix([[0, 0], [mu, 1]])) == sp.zeros(2, 2)
    assert sp.simplify(jb - g * sp.Matrix([[0, -mu], [0, 1]])) == sp.zeros(2, 2)
    # JB == R(JA): the derived pair satisfies the reciprocity transform
    assert sp.simplify(reciprocity_transform(ja) - jb) == sp.zeros(2, 2)


def test_perrin_theorem_general_symbolic():
    """For ANY J and any states u, v: amp_B = (sig u*)^dag R(J) (sig v*)
    == v^dag J u = amp_A — hence I_B = I_A for normalized states
    (Perrin / Lorentz reciprocity, paper Eqs. 8-13 generalized)."""
    j = sp.Matrix(2, 2, sp.symbols("j00 j01 j10 j11", complex=True))
    u = sp.Matrix(sp.symbols("ux uy", complex=True))
    v = sp.Matrix(sp.symbols("vx vy", complex=True))
    sig = sp.diag(1, -1)
    amp_a = (v.H * j * u)[0, 0]
    amp_b = ((sig * u.conjugate()).H * reciprocity_transform(j)
             * (sig * v.conjugate()))[0, 0]
    assert sp.simplify(sp.expand(amp_a - amp_b)) == 0


def test_perrin_paper_special_case_eq8_13():
    """Paper's construction: E1 = (x,y) into Case A; Case B feeds V and
    analyzes with the reversed elliptical polarizer of E1 -> I_B = I_A."""
    x, y = sp.symbols("xs ys", complex=True)
    al = sp.symbols("al_s", complex=True)
    ja, jb = case_A_jones(al, BC, E1S), case_B_jones(al, BC, E1S)
    e1v = sp.Matrix([x, y])
    out_a = ja * e1v
    i_a = sp.expand((out_a.H * out_a)[0, 0])
    pol = sp.Matrix([[x * sp.conjugate(x), x * sp.conjugate(y)],
                     [sp.conjugate(x) * y, y * sp.conjugate(y)]])
    out_b = reciprocity_transform(pol) * jb * sp.Matrix([0, 1])
    i_b = sp.expand((out_b.H * out_b)[0, 0])
    norm = x * sp.conjugate(x) + y * sp.conjugate(y)
    assert sp.simplify(i_b - norm * i_a) == 0  # paper Eq. 13


# -- gamma map -------------------------------------------------------------------

def test_forward_gamma_theorem():
    """gamma == i e1 a1 a2 Delta1 (1 - e2^2)/(2N) — with the derived J."""
    got = forward_gamma_general(TH, F1, F2, A1, A2, AC, BC, E1S, E2S)
    _, n, dd1 = _paper_a11()
    pred = sp.I * E1S * A1 * A2 * dd1 * (1 - E2S ** 2) / (2 * n)
    assert sp.simplify(sp.expand_trig(sp.together(got - pred))) == 0


def test_forward_gamma_zero_conditions():
    got = forward_gamma_general(TH, F1, F2, A1, A2, AC, BC, E1S, E2S)
    assert sp.simplify(got.subs(E2S, 1)) == 0       # co-planar
    assert sp.simplify(got.subs(E2S, -1)) == 0      # half-wavelength offset
    assert sp.simplify(got.subs(A2, 0)) == 0        # no second dipole
    # Delta1 = 0 example: theta = 0 and phi1 = 0 (d2s = 0, b_ = 0)
    assert sp.simplify(got.subs({TH: 0, F1: 0})) == 0
    # coupled-but-gamma-blind branch (review sug. 3): theta = pi/2 makes
    # Delta1 = 0 with the coupling STILL PRESENT (both dipoles vertical)
    assert sp.simplify(got.subs(TH, sp.pi / 2)) == 0


def test_case_a_gamma_signature():
    """90-degree direction: gamma(JA) = -i g mu / 2 != 0 — the asymmetric-
    scattering gamma signature (known fact, recorded; no novelty claim)."""
    al = sp.symbols("al_s", complex=True)
    ja = case_A_jones(al, BC, E1S)
    delta = -BC / 2
    g = al / (1 - E1S ** 2 * al ** 2 * delta ** 2)
    mu = E1S * al * delta
    assert sp.simplify(jones_to_hvector(ja).gamma + sp.I * g * mu / 2) == 0


# -- numeric layer + guards ---------------------------------------------------------

def test_numeric_matches_symbolic_seeded():
    rng = np.random.default_rng(20260713)
    for _ in range(3):
        th, f1, f2 = rng.uniform(0, 2 * np.pi, 3)
        a1, a2, ac, bc = (complex(x, y) * 0.3 for x, y in
                          rng.standard_normal((4, 2)))
        e1v = np.exp(1j * rng.uniform(0, 2 * np.pi))
        e2v = np.exp(1j * rng.uniform(0, 2 * np.pi))
        num = forward_jones_numeric(th, f1, f2, a1, a2, ac, bc, e1v, e2v)
        sym = forward_jones_general(
            sp.Float(th), sp.Float(f1), sp.Float(f2), a1, a2, ac, bc,
            sp.sympify(e1v), sp.sympify(e2v))
        sym = np.array(sp.matrix2numpy(sym.evalf(), dtype=complex))
        assert np.max(np.abs(num - sym)) < 1e-10


def test_numeric_guards():
    with pytest.raises(ValueError, match="finite"):
        forward_jones_numeric(np.nan, 0, 0, 0.1, 0.1, 0.1, 0.1, 1, 1)
    # exact resonance: theta=pi/2 (c=1), phi1=0 -> d1s=A=0.5, d2s=0:
    # N = 1 - e1^2 a1 a2 d1s^2 = 1 - 4*0.25 = 0
    with pytest.raises(ValueError, match="resonance"):
        forward_jones_numeric(np.pi / 2, 0.0, 0.0, 2.0, 2.0, 0.5, 0.0, 1.0, 1.0)
