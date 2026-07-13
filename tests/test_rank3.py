"""Stage-10: rank-3 three-term decomposition — deriver, solver, bridge.

M34 note: no paper table exists for this zone. The symbolic anchors below
are the HAND-DERIVED, probe-verified formulas fixed in spec-10 §0; the
deriver must reproduce them exactly (layer ii of the M34 replacement for
the K28 paper anchor)."""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.decomposition.derive import generic_hermitian
from organon_mueller.decomposition.rank3 import (
    PAIR_12,
    PAIR_13,
    PAIR_23,
    RANK3_PAIRS,
    decompose_rank3,
    derive_rank3,
    propose_decompositions,
    sweep_rank3,
)
from organon_mueller.decomposition.solve import DecompositionError, decompose

RNG_SEED = 20260713

_H = generic_hermitian()
_h = lambda i, j: _H[i, j]  # noqa: E731


# -- deriver == hand formulas (M34 layer ii) ------------------------------------

def test_pair12_matches_hand_formulas():
    d = derive_rank3(PAIR_12)
    exprs = dict(d.exprs)
    c_hand = (_h(1, 1) * _h(2, 2) - _h(1, 2) * _h(2, 1)) / (
        _h(1, 1) + _h(2, 2) - _h(1, 2) - _h(2, 1))
    w_hand = (_h(0, 2) * (_h(1, 1) - c_hand) - _h(0, 1) * (_h(1, 2) - c_hand)) / (
        _h(1, 1) - _h(1, 2))
    assert sp.simplify(exprs["center"] - c_hand) == 0
    assert sp.simplify(exprs["edge"] - w_hand) == 0


def test_pair13_matches_hand_formulas():
    d = derive_rank3(PAIR_13)
    exprs = dict(d.exprs)
    c_hand = (_h(1, 1) * _h(2, 2) - _h(1, 2) * _h(2, 1)) / (
        _h(1, 1) + _h(2, 2) + _h(1, 2) + _h(2, 1))
    w_hand = (_h(0, 1) * (_h(1, 2) + c_hand) - _h(0, 2) * (_h(1, 1) - c_hand)) / (
        _h(1, 1) + _h(1, 2))
    assert sp.simplify(exprs["center"] - c_hand) == 0
    assert sp.simplify(exprs["edge"] - w_hand) == 0


def test_pair23_matches_hand_formulas():
    d = derive_rank3(PAIR_23)
    exprs = dict(d.exprs)
    sigma_hand = (_h(0, 0) * _h(3, 3) - _h(0, 3) * _h(3, 0)) / (
        _h(0, 0) + _h(3, 3) - _h(0, 3) - _h(3, 0))
    p_hand = (sigma_hand * (_h(3, 1) - _h(0, 1)) + _h(0, 1) * _h(3, 0)
              - _h(0, 0) * _h(3, 1)) / (_h(3, 0) - _h(0, 0))
    m_hand = (sigma_hand * (_h(3, 2) - _h(0, 2)) + _h(0, 2) * _h(3, 0)
              - _h(0, 0) * _h(3, 2)) / (_h(3, 0) - _h(0, 0))
    s_hand = _h(1, 1) - (_h(0, 1) - p_hand) * (_h(1, 3) - sp.conjugate(p_hand)) / (
        _h(0, 3) - sigma_hand)
    d_hand = _h(1, 2) - (_h(0, 2) - m_hand) * (_h(1, 3) - sp.conjugate(p_hand)) / (
        _h(0, 3) - sigma_hand)
    for name, hand in (("sigma", sigma_hand), ("p", p_hand), ("m", m_hand),
                       ("s", s_hand), ("d", d_hand)):
        assert sp.simplify(exprs[name] - hand) == 0, f"{name} mismatch"


def test_deriver_rejects_unknown_pair():
    with pytest.raises(ValueError):
        derive_rank3(("type2", "type2"))


# -- synthetic construction helpers ----------------------------------------------

def _template(sym, x, w):
    from organon_mueller.decomposition.rank3 import _template_numeric
    return _template_numeric(sym, x, w)


def _sym_pure(sym, rng):
    total = 1.0 if sym == "type1" else 0.5
    x = float(rng.uniform(0.15, total - 0.15))
    w = np.sqrt(x * (total - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    return _template(sym, x, w)


def _gen_pure(rng):
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    return np.outer(u, u.conj()), u


def _mix(pair, rng):
    h_a, h_b = _sym_pure(pair[0], rng), _sym_pure(pair[1], rng)
    h_g, _ = _gen_pure(rng)
    a_a, a_b = float(rng.uniform(0.2, 0.4)), float(rng.uniform(0.2, 0.4))
    a_g = 1 - a_a - a_b
    return (a_a * h_a + a_b * h_b + a_g * h_g,
            (a_a, a_b, a_g), (h_a, h_b, h_g))


# -- roundtrips -------------------------------------------------------------------

@pytest.mark.parametrize("pair", RANK3_PAIRS, ids=lambda p: "+".join(p))
def test_synthetic_roundtrip(pair):
    rng = np.random.default_rng(RNG_SEED)
    for _ in range(3):
        cov, alphas, comps = _mix(pair, rng)
        r = decompose_rank3(cov, pair)
        assert max(abs(r.alphas[i] - alphas[i]) for i in range(3)) < 1e-8
        for i in range(3):
            assert np.max(np.abs(r.h_components[i] - comps[i])) < 1e-6
        if pair == PAIR_23:
            assert r.consistency_residual is not None
            assert r.consistency_residual < 1e-10


# -- guards -----------------------------------------------------------------------

def test_trace_guard():
    rng = np.random.default_rng(RNG_SEED)
    cov, *_ = _mix(PAIR_12, rng)
    with pytest.raises(DecompositionError, match="trace"):
        decompose_rank3(2.0 * cov, PAIR_12)


def test_rank_guard_rejects_rank2():
    rng = np.random.default_rng(RNG_SEED)
    h1 = _sym_pure("type1", rng)
    h2, _ = _gen_pure(rng)
    cov = 0.4 * h1 + 0.6 * h2
    with pytest.raises(DecompositionError, match="rank"):
        decompose_rank3(cov, PAIR_12)


def test_same_type_pair_rejected_at_api():
    with pytest.raises(ValueError, match="pair"):
        decompose_rank3(np.eye(4) / 4, ("type1", "type1"))


def test_degenerate_generic_pure_hits_denominator_guard():
    """If the generic pure fails to carry the missing anisotropy (here
    u1 = u2 makes the {1,2} center denominator alpha_G*|u1-u2|^2 vanish),
    the guard must fire, not return junk."""
    rng = np.random.default_rng(RNG_SEED)
    h_a, h_b = _sym_pure("type1", rng), _sym_pure("type2", rng)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u[2] = u[1]  # degeneracy: u1 == u2
    u /= np.linalg.norm(u)
    h_g = np.outer(u, u.conj())
    cov = 0.3 * h_a + 0.35 * h_b + 0.35 * h_g
    with pytest.raises(DecompositionError):
        decompose_rank3(cov, PAIR_12)


@pytest.mark.parametrize("src", RANK3_PAIRS, ids=lambda p: "+".join(p))
def test_cross_pair_honesty(src):
    """Wrong pair on any pair's data: must raise (delegation, realness,
    domain or consistency guards) — never a silent plausible-but-wrong
    answer. Full 3x2 direction matrix (review defect 4)."""
    rng = np.random.default_rng(RNG_SEED)
    cov, *_ = _mix(src, rng)
    for pair in RANK3_PAIRS:
        if pair == src:
            continue
        with pytest.raises(DecompositionError):
            decompose_rank3(cov, pair)


def test_k32_consistency_guard_fires():
    """K32 (review defect 1 — the MANDATORY overdetermination check needs
    its own regression test): an all-REAL random rank-3 covariance sails
    past the realness guards (s, d real by construction) and must be
    rejected by |k2+e3-sigma|. Seed 0 verified to reach exactly this
    guard."""
    rng = np.random.default_rng(0)
    us = [rng.standard_normal(4) for _ in range(3)]
    ws = rng.uniform(0.2, 0.4, 2)
    weights = [*ws, 1 - ws.sum()]
    cov = sum(w * np.outer(u, u) / (u @ u) for w, u in zip(weights, us))
    with pytest.raises(DecompositionError, match="consistency guard"):
        decompose_rank3(cov, PAIR_23)


def test_degenerate_u0_equals_u3_hits_sigma_denominator():
    """Spec-10 acceptance: the u0 = u3 degeneracy (generic pure lacking
    the {2,3} corner anisotropy alpha_G*|u0-u3|^2) must hit the
    denominator guard (review defect 4)."""
    rng = np.random.default_rng(RNG_SEED)
    h_a, h_b = _sym_pure("type2", rng), _sym_pure("type3", rng)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u[3] = u[0]
    u /= np.linalg.norm(u)
    cov = 0.3 * h_a + 0.35 * h_b + 0.35 * np.outer(u, u.conj())
    with pytest.raises(DecompositionError, match="denominator"):
        decompose_rank3(cov, PAIR_23)


def test_center_only_pure_boundary_family():
    """Review defect 2: a type-2 pure with edge w = 0 exactly (u along
    (0,1,1,0)/sqrt(2) — center-only, a legitimate Table-1 point) used to
    collapse the rebuilt template to the zero matrix and reject valid
    data with a misleading trace message. Must now decompose exactly."""
    rng = np.random.default_rng(RNG_SEED)
    u_b = np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2)
    h_b = np.outer(u_b, u_b.conj())
    h_a = _sym_pure("type1", rng)
    h_g, u = _gen_pure(rng)
    cov = 0.3 * h_a + 0.35 * h_b + 0.35 * h_g
    r = decompose_rank3(cov, PAIR_12)
    assert abs(r.alphas[1] - 0.35) < 1e-8
    assert np.max(np.abs(r.h_components[1] - h_b)) < 1e-8


def test_non_finite_input_guarded():
    """Review defect 3: NaN passes |trace-1| comparisons — an explicit
    finiteness guard must reject, and the bridge must report a reason
    instead of crashing."""
    bad = np.eye(4, dtype=complex) / 4
    bad[0, 0] = np.nan
    with pytest.raises(DecompositionError, match="non-finite"):
        decompose_rank3(bad, PAIR_12)
    with pytest.raises(DecompositionError, match="non-finite"):
        decompose(covariance=bad, symmetry="type1")
    report = propose_decompositions(bad)
    assert report.successes == []
    assert any("non-finite" in reason for _, reason in report.failures)


def test_two_same_type_components_rejected():
    """Data with TWO type-2 pures + generic (rank 3) offered to {2,3}:
    the recovered type-3 part collapses (v3 ~ 0) and a domain or
    consistency guard must reject."""
    rng = np.random.default_rng(RNG_SEED)
    cov = (0.3 * _sym_pure("type2", rng) + 0.3 * _sym_pure("type2", rng)
           + 0.4 * _gen_pure(rng)[0])
    with pytest.raises(DecompositionError):
        decompose_rank3(cov, PAIR_23)


# -- bridge v0 ---------------------------------------------------------------------

def test_propose_on_rank2_finds_fundamental():
    rng = np.random.default_rng(RNG_SEED)
    h1 = _sym_pure("type1", rng)
    h2, _ = _gen_pure(rng)
    report = propose_decompositions(0.4 * h1 + 0.6 * h2)
    assert report.rank == 2
    labels = [label for label, _ in report.successes]
    assert "type1" in labels
    # every non-success carries a reason (K21: no silent elimination)
    assert all(reason for _, reason in report.failures)


def test_propose_on_rank3_finds_the_right_pair():
    rng = np.random.default_rng(RNG_SEED)
    cov, alphas, _ = _mix(PAIR_13, rng)
    report = propose_decompositions(cov)
    assert report.rank == 3
    labels = [label for label, _ in report.successes]
    assert "type1+type3" in labels
    result = dict(report.successes)["type1+type3"]
    assert max(abs(result.alphas[i] - alphas[i]) for i in range(3)) < 1e-8
    assert all(reason for _, reason in report.failures)


def test_propose_unsupported_rank_reports_reason():
    report = propose_decompositions(np.eye(4) / 4)  # rank 4
    assert report.rank == 4
    assert report.successes == []
    assert any("rank 4" in reason for _, reason in report.failures)


# -- sweep artifact (K21) -----------------------------------------------------------

def test_sweep_rank3_deterministic_and_clean():
    first = sweep_rank3(trials_per_pair=2)
    second = sweep_rank3(trials_per_pair=2)
    assert first == second  # fully deterministic
    recovered = [e for e in first["entries"] if e.get("status") == "recovered"]
    assert len(recovered) == 6  # 3 pairs x 2 trials
    assert all(e["alpha_error"] < 1e-8 for e in recovered)
    assert all(e["component_error"] < 1e-6 for e in recovered)
    # controls: rank-2 data must be rejected outright; rank-3 same-pair
    # data may be rejected OR yield a VERIFIED alternative decomposition
    # (stage-10 non-uniqueness finding) — but never an unverified accept
    controls = [e for e in first["entries"] if "control" in e]
    assert len(controls) == 6
    for e in controls:
        if e["control"] == "rank2_type1":
            assert e["status"] == "rejected" and e["reason"]
        else:
            assert e["status"] in ("rejected", "accepted_alternative_verified")
            if e["status"] == "accepted_alternative_verified":
                assert e["reconstruction_error"] < 1e-10
                assert e["max_purity_defect"] < 1e-8
    # the finding must actually appear in this sweep (it does with this
    # seed: {1,2} re-splits the two-type-2 control exactly)
    assert any(e["status"] == "accepted_alternative_verified" for e in controls)
    assert "novelty" in first["note"] or "claim" in first["note"]
