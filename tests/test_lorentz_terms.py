"""Milestone L4 (FROZEN-7): term language + THE SELF-RECOVERY GATE.

The credibility precondition of the L5 discovery sweep (v2's A5
recovery-campaign tradition): before hunting new identities, the
machinery must find the ten known ones ITSELF — numeric enumeration
that never consults the known registry, then symbolic certification
through a generic prover independent of ``identities.py``.
"""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.lorentz import METRIC, z_bar_matrix, z_matrix
from organon_mueller.lorentz.terms import (
    KNOWN_TEN,
    NAMES,
    SEEDS,
    certify,
    classify_all,
    letter_matrices,
    recovery_gate,
)

A = sp.symbols("d0 d1 d2 d3", complex=True)


def test_letters_are_the_advertised_operations():
    """Each of the 8 letters is exactly the advertised conjugation-type
    of Z or Z̄ at generic complex α."""
    L = letter_matrices(A)
    z, zb = z_matrix(A), z_bar_matrix(A)
    want = {
        "Z": z, "Zc": z.conjugate(), "Zt": z.T, "Zd": z.conjugate().T,
        "Zb": zb, "Zbc": zb.conjugate(), "Zbt": zb.T,
        "Zbd": zb.conjugate().T,
    }
    assert set(L) == set(NAMES) == set(want)
    for k in want:
        assert sp.expand(L[k] - want[k]) == sp.zeros(4)


def test_base_alias_facts_locked():
    """Why the g-conjugates are NOT separate bases: Λ̄ = gΛᵀg (L2
    bonus theorem) and its transpose corollary Λ̄ᵀ = gΛg."""
    z, zb = z_matrix(A), z_bar_matrix(A)
    lam = sp.expand(z * z.conjugate())
    lamb = sp.expand(zb * zb.conjugate())
    assert sp.expand(lamb - METRIC * lam.T * METRIC) == sp.zeros(4)
    assert sp.expand(lamb.T - METRIC * lam * METRIC) == sp.zeros(4)


def test_classification_is_deterministic_and_sane():
    """The two fixed seeds must agree (classify_all raises otherwise),
    and the 128-sandwich space partitions into the locked shape."""
    cls = classify_all()
    assert len(cls) == 128
    counts = {}
    for kind, _ in cls.values():
        counts[kind] = counts.get(kind, 0) + 1
    assert counts == {"match": 16, "expansion-unmatched": 24,
                      "no-expansion": 88}


def test_gate_finds_all_ten_knowns_with_exact_classes():
    """THE GATE, part 1: the registry-blind enumeration finds every
    known identity with exactly its known (scalar, base) class."""
    cls = classify_all()
    for k, v in KNOWN_TEN.items():
        kind, hit = cls[k]
        assert kind == "match" and hit == v, (k, kind, hit)


def test_gate_certifies_all_ten_symbolically():
    """THE GATE, part 2: the generic symbolic certifier proves each of
    the ten — a code path independent of identities.py."""
    for (x, mid, y), (s, b) in KNOWN_TEN.items():
        assert certify(x, mid, y, s, b), (x, mid, y, s, b)


def test_negative_control_unmatched_sandwich():
    """A sandwich with no identity behind it must NOT classify as a
    match (screen soundness)."""
    kind, hit = classify_all()[("Z", "S", "Z")]
    assert kind != "match" and hit is None


def test_certifier_rejects_wrong_claims():
    """The certifier must be falsifiable: a wrong base for LT1 and a
    wrong scalar for LT4 both fail; bad labels raise readable errors."""
    assert not certify("Zd", "S", "Z", "1", "LamT")
    assert not certify("Zt", "S", "Zbt", "qbar", "I")
    with pytest.raises(ValueError, match="mid"):
        certify("Zd", "X", "Z", "1", "Lam")
    with pytest.raises(ValueError, match="letters"):
        certify("W", "S", "Z", "1", "Lam")
    with pytest.raises(ValueError, match="scalar"):
        certify("Zd", "S", "Z", "2", "Nope")


def test_seed_quality_guard():
    """Both seeds give genuinely complex α with |q| bounded away from
    the null cone (q ≠ q̄ matters: it separates LT2/3 from LT4/5)."""
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        a = rng.normal(size=4) + 1j * rng.normal(size=4)
        q = a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2
        assert abs(q) > 0.1
        assert abs(q - np.conj(q)) > 0.1


def test_recovery_gate_verdict():
    """End to end: the gate passes, and the extra matches beyond the
    ten are exactly the six Λ-family variants counted for L5 (counts
    only — statement-level claims are L5 scope)."""
    g = recovery_gate()
    assert g["passed"] is True
    assert all(g["found"].values()) and all(g["certified"].values())
    assert g["class_counts"] == {"match": 16, "expansion-unmatched": 24,
                                 "no-expansion": 88}
    assert len(g["extra_matches"]) == 6
