"""Stage-11 (iter): bridge v1 scores, guard-generator meta-test, and the
Kuntman-package demo smoke test."""
import importlib.util
import pathlib

import numpy as np
import pytest

from organon_mueller.decomposition.rank3 import (
    PAIR_13,
    RANK3_PAIRS,
    _template_numeric,
    propose_decompositions,
)

RNG_SEED = 20260713
ROOT = pathlib.Path(__file__).resolve().parent.parent


def _rank3_mix(pair, rng):
    parts = []
    for sym in pair:
        total = 1.0 if sym == "type1" else 0.5
        x = float(rng.uniform(0.15, total - 0.15))
        w = np.sqrt(x * (total - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
        parts.append(_template_numeric(sym, x, w))
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    parts.append(np.outer(u, u.conj()))
    return 0.3 * parts[0] + 0.35 * parts[1] + 0.35 * parts[2]


# -- bridge v1: structure scores --------------------------------------------------

def test_scores_present_for_every_attempted_hypothesis():
    rng = np.random.default_rng(RNG_SEED)
    report = propose_decompositions(_rank3_mix(PAIR_13, rng))
    assert report.rank == 3
    expected = {"+".join(p) for p in RANK3_PAIRS}
    assert set(report.scores) == expected
    attempted = {label for label, _ in report.successes}
    attempted |= {label for label, _ in report.failures}
    assert attempted == expected  # ordering never eliminates (spec-11)


def test_scores_deterministic_and_true_hypothesis_scored():
    rng1 = np.random.default_rng(RNG_SEED)
    rng2 = np.random.default_rng(RNG_SEED)
    r1 = propose_decompositions(_rank3_mix(PAIR_13, rng1))
    r2 = propose_decompositions(_rank3_mix(PAIR_13, rng2))
    assert r1.scores == r2.scores
    score = r1.scores["type1+type3"]
    assert np.isfinite(score) and score > 0
    assert "type1+type3" in [label for label, _ in r1.successes]


def test_success_set_unchanged_by_scoring():
    """Scores ORDER, never eliminate: success set == the set that passes
    the exact solvers, regardless of score values."""
    rng = np.random.default_rng(RNG_SEED)
    cov = _rank3_mix(PAIR_13, rng)
    report = propose_decompositions(cov)
    from organon_mueller.decomposition.rank3 import decompose_rank3
    from organon_mueller.decomposition.solve import DecompositionError

    exact = set()
    for pair in RANK3_PAIRS:
        try:
            decompose_rank3(cov, pair)
            exact.add("+".join(pair))
        except DecompositionError:
            pass
    assert {label for label, _ in report.successes} == exact


def test_successes_ordered_by_score():
    rng = np.random.default_rng(RNG_SEED)
    report = propose_decompositions(_rank3_mix(PAIR_13, rng))
    ordered = [report.scores[label] for label, _ in report.successes]
    assert ordered == sorted(ordered, reverse=True)


def test_rank2_scores_cover_fundamentals_and_composites():
    rng = np.random.default_rng(RNG_SEED)
    total, x = 1.0, float(rng.uniform(0.15, 0.85))
    w = np.sqrt(x * (total - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h1 = _template_numeric("type1", x, w)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    cov = 0.4 * h1 + 0.6 * np.outer(u, u.conj())
    report = propose_decompositions(cov)
    assert report.rank == 2
    assert set(report.scores) == {
        "type1", "type2", "type3", "type1-2", "type1-3", "type2-3"}


# -- guard-generator meta-test (design-note obligation 1, structural form) --------

def test_every_guard_key_has_both_generators():
    pytest.importorskip("egglog")
    from organon_mueller.discovery.guards import (
        GUARD_KEYS,
        guarded_random_hvector,
        guarded_symbolic_hvector,
    )

    rng = np.random.default_rng(0)
    for key in GUARD_KEYS:
        hv_num = guarded_random_hvector(rng, key)
        hv_sym = guarded_symbolic_hvector("x", key)
        # both generators exist and produce nonzero states
        assert any(p != 0 for p in (hv_num.tau, hv_num.alpha,
                                    hv_num.beta, hv_num.gamma))
        assert hv_sym.to_z().free_symbols
    # the other direction of "birebir": keys OUTSIDE the vocabulary must
    # be rejected by both generators (no orphan branches)
    with pytest.raises(ValueError):
        guarded_random_hvector(rng, "not_a_guard")
    with pytest.raises(ValueError):
        guarded_symbolic_hvector("x", "not_a_guard")


# -- demo smoke test (canonical: examples/demo.py; the feedback package
# ships a shim at docs/kuntman-package/demo.py that re-exports main) -----------------

@pytest.mark.parametrize("rel", [
    ("examples", "demo.py"),                 # canonical general demo
    ("docs", "kuntman-package", "demo.py"),  # feedback-package shim
], ids=["canonical", "package-shim"])
def test_demo_runs_and_matches_paper(rel):
    demo_path = ROOT.joinpath(*rel)
    spec = importlib.util.spec_from_file_location("demo_under_test",
                                                  demo_path)
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)

    results = demo.main()
    s6 = results["section6"]
    assert abs(s6["alpha1"] - 0.3) < 1e-3
    assert s6["m1_max_err"] < 1e-3 and s6["m2_max_err"] < 1e-3
    r3 = results["rank3_candidate_zone"]
    assert max(abs(a - b) for a, b in
               zip(r3["alphas_true"], r3["alphas_recovered"])) < 1e-8
    assert r3["component_max_err"] < 1e-6
    br = results["bridge"]
    assert br["rank"] == 3 and "type1+type2" in br["successes"]
    assert set(br["failures"]) | set(br["successes"]) == set(br["scores"])
    dp = results["dipoles"]  # stage-15 addendum section
    assert dp["decomposition_eq25_err"] < 1e-10
    assert dp["gamma_map"]["coplanar"] < 1e-12
    assert dp["gamma_map"]["offplane"] > 1e-6
    en = dp["ensemble"]
    # margin 2.5x at n=400 (review: numpy stream stability caveat;
    # pinned-seed ratio ~1687x, 47-seed sweep worst case 4.39x)
    assert en["chiral_mean_abs"] > 2.5 * en["achiral_mean_abs"]
    assert en["uncoupled_pointwise"] < 1e-14
