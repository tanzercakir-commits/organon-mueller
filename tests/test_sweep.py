"""Stage-6: sweep campaign module (small CI config — K22)."""
import json

import pytest

pytest.importorskip("egglog")

from organon_mueller.discovery.sweep import (  # noqa: E402
    SweepConfig,
    outcomes_to_json,
    run_one,
    run_sweep,
)


def test_small_sweep_deterministic():
    config = SweepConfig(atom_names=("a", "b"), max_size=5)
    first, second = run_one(config), run_one(config)
    # conj_normal defaults to True: pruned size-5 count is 36 (not 66 unpruned)
    assert first.n_terms == second.n_terms == 36
    assert first.verified_count == second.verified_count
    assert first.underivable_pairs == second.underivable_pairs == []
    assert first.refuted_count == 0 and first.status == "completed"
    assert first.fingerprint_seed == second.fingerprint_seed


def test_budget_skip_is_recorded_not_dropped():
    configs = [
        SweepConfig(atom_names=("a", "b"), max_size=4),
        SweepConfig(atom_names=("a", "b"), max_size=5),
    ]
    outcomes = run_sweep(configs, budget_seconds=0.0)
    assert len(outcomes) == 2  # K21: nothing silently dropped
    assert all(o.status == "skipped_budget" for o in outcomes)
    # skipped outcomes carry NO observation fields (stage-6 review):
    # a skipped config must never read as a real "0 underivable"
    assert all(o.n_terms is None and o.underivable_pairs is None for o in outcomes)


def test_completed_outcome_carries_reproduction_inputs():
    outcome = run_one(SweepConfig(atom_names=("a", "b"), max_size=4))
    assert outcome.fingerprint_seed == 424242
    assert outcome.numeric_seed == 20260713 and outcome.numeric_draws == 3


def test_json_artifact_roundtrip():
    outcomes = run_sweep([SweepConfig(atom_names=("a", "b"), max_size=4)])
    payload = json.loads(outcomes_to_json(outcomes, environment_note="test env"))
    assert payload["environment_note"] == "test env"
    entry = payload["outcomes"][0]
    assert entry["status"] == "completed"
    assert entry["atom_names"] == ["a", "b"]
    assert set(entry) >= {
        "n_terms", "n_buckets", "verified_count", "refuted_count",
        "underivable_pairs", "fingerprint_seed", "total_seconds",
    }
