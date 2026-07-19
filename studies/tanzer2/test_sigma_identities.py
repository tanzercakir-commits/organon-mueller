"""Locks the TANZER_2 result. Run: pytest studies/tanzer2/ -q
(outside the shipped package's default test path — this is a study, not
a library feature, so it does not touch the suite count or its guards).
"""
import numpy as np
import sympy as sp

from sigma_identities import (
    NAMES,
    SIGMA,
    TASK1,
    commutation_lemma,
    commuting_elements,
    det_Z_is_alpha_squared,
    set_S,
    sigma_is_hermitian,
    summary,
    table,
    z_and_zinv,
)


def _zero(m):
    return sp.expand(m) == sp.zeros(4)


# -- the structural facts (exact) -------------------------------------------

def test_sigma_hermitian_so_star_equals_transpose():
    assert sigma_is_hermitian()


def test_the_commutation_lemma():
    """The heart: (Sigma^mu)^T commutes with Sigma^nu, all 16 pairs."""
    assert commutation_lemma()


def test_det_Z_is_alpha_dot_alpha_squared_not_alpha_dot_alpha():
    """Honest precision: det(Z) = (alpha.alpha)^2, so the brief's
    'det(Z) = alpha_0^2 - ...' is the square root of the true determinant;
    the intended constraint alpha.alpha = 1 is what the study uses."""
    assert det_Z_is_alpha_squared()
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    Z, _ = z_and_zinv(a)
    q = a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2
    assert sp.expand(Z.det() - q) != 0            # NOT equal to alpha.alpha


def test_family_split_is_exactly_the_transpose_built_four():
    comm = commuting_elements()
    assert {n for n, ok in comm.items() if ok} == {
        "Z*", "Z^T", "(Z^-1)*", "(Z^-1)^T"}
    assert {n for n, ok in comm.items() if not ok} == {
        "Z", "Z^-1", "Zdag", "(Z^-1)dag"}


# -- the mu=0 necessity and the mu>=1 obstruction ---------------------------

def test_mu0_forces_A_times_B_equals_identity():
    """Sigma^0 = I, so Sigma^0 = A Sigma^0 B reduces to A B = I: the
    identity can hold only when B = A^{-1}. Shown on the constraint for a
    passing pair (Z*, (Z^-1)*) and a Sigma-built pair (Z, Z^-1)."""
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    S = set_S(a)
    q = a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2
    # A B = (scalar) I in every candidate case; = I on alpha.alpha = 1
    assert _zero(S["Z*"] * S["(Z^-1)*"] - sp.conjugate(q) * sp.eye(4))
    assert _zero(S["Z"] * S["Z^-1"] - q * sp.eye(4))


def test_sigma_built_A_gives_a_rotation_not_the_identity():
    """A Sigma-built element passes mu=0 (A A^{-1} = I) but FAILS mu>=1:
    Z Sigma^k Z^{-1} is a genuine mix of the basis, not Sigma^k. This is
    why the four Sigma-built (A, A^{-1}) pairs are NOT identities."""
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    Z, Zi = z_and_zinv(a)
    assert not _zero(Z * SIGMA[1] * Zi - SIGMA[1])


# -- the 64-trial table -----------------------------------------------------

def test_task1_four_identities_hold():
    t = table()
    for A, B in TASK1:
        assert t[(A, B)], (A, B)


def test_task2_exactly_the_four_given_no_more():
    """The whole point of Task 2: within S, no NEW identities of the form
    Sigma^mu = A Sigma^mu B exist beyond the four given ones."""
    t = table()
    yes = {k for k, v in t.items() if v}
    assert yes == set(TASK1)
    assert len(yes) == 4


def test_table_is_full_8x8_and_deterministic():
    t = table()
    assert len(t) == 64
    assert all((an, bn) in t for an in NAMES for bn in NAMES)
    # a third independent constraint point agrees (no coincidence)
    t3 = table(seeds=(20260718, 20260720))
    assert {k for k, v in t3.items() if v} == set(TASK1)


def test_summary_is_internally_consistent():
    s = summary()
    assert s["sigma_hermitian"] and s["commutation_lemma"]
    assert s["det_Z_is_alpha_squared"]
    assert s["task1_all_hold"] and s["only_task1"] and s["count"] == 4
