"""Sweep campaigns (stage 6): configured discovery runs with durable,
reproducible JSON artifacts (decisions M24/M25).

A sweep is a list of configs run through the v1.2 engine. Outcomes carry
everything needed to reproduce (config + seeds are deterministic by
construction, rules K12/K14/K21) and the full render of any underivable
pair — the novelty channel feeding docs/novelty-protocol.md. An EMPTY
novelty channel is a first-class result (M24): empirical completeness of
the axiom set for the swept fragment.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field

from .engine import DiscoveryEngine
from .fingerprint import FINGERPRINT_SEED

__all__ = ["SweepConfig", "SweepOutcome", "run_sweep", "outcomes_to_json"]


@dataclass(frozen=True)
class SweepConfig:
    atom_names: tuple[str, ...]
    max_size: int
    conj_normal: bool = True
    certify: str = "underivable"


@dataclass
class SweepOutcome:
    atom_names: tuple[str, ...]
    max_size: int
    conj_normal: bool
    certify: str
    fingerprint_seed: int
    #: numeric verification parameters (K21: the artifact carries every
    #: reproduction input, not just the fingerprint seed)
    numeric_seed: int | None = None
    numeric_draws: int | None = None
    status: str = "completed"  # or "skipped_budget"
    #: observation fields are None (JSON null) when status != "completed",
    #: so a skipped config can never be mistaken for a real observation
    #: (stage-6 review)
    n_terms: int | None = None
    n_buckets: int | None = None
    verified_count: int | None = None
    refuted_count: int | None = None
    demoted_count: int | None = None
    fingerprint_collisions: int | None = None
    numeric_false_negatives: int | None = None
    #: full renders — the novelty channel (empty = completeness observation)
    underivable_pairs: list[str] | None = None
    harvest_seconds: float | None = None
    total_seconds: float | None = None


def run_one(config: SweepConfig) -> SweepOutcome:
    import inspect

    from .interpret import terms_numerically_equal

    sig = inspect.signature(terms_numerically_equal).parameters
    start = time.perf_counter()
    result = DiscoveryEngine(
        atom_names=config.atom_names,
        max_size=config.max_size,
        conj_normal=config.conj_normal,
        certify=config.certify,
    ).run()
    total = time.perf_counter() - start
    return SweepOutcome(
        numeric_seed=sig["seed"].default,
        numeric_draws=sig["draws"].default,
        atom_names=config.atom_names,
        max_size=config.max_size,
        conj_normal=config.conj_normal,
        certify=config.certify,
        fingerprint_seed=FINGERPRINT_SEED,
        n_terms=result.n_terms,
        n_buckets=result.n_buckets,
        verified_count=len(result.verified),
        refuted_count=len(result.refuted),
        demoted_count=len(result.demoted_by_symbolic),
        fingerprint_collisions=result.fingerprint_collisions,
        numeric_false_negatives=result.numeric_false_negatives,
        underivable_pairs=[p.render() for p in result.underivable],
        harvest_seconds=round(result.harvest_seconds, 2),
        total_seconds=round(total, 2),
    )


def run_sweep(
    configs: list[SweepConfig], budget_seconds: float | None = None
) -> list[SweepOutcome]:
    """Run configs in order. The budget is checked only BETWEEN configs: a
    config that starts always runs to completion and may overshoot the
    budget (there is no mid-run cutoff). Configs reached after the budget
    is exhausted are recorded as status="skipped_budget" with null
    observation fields (K21: nothing silently dropped, nothing conflatable
    with a real observation)."""
    outcomes: list[SweepOutcome] = []
    started = time.perf_counter()
    for config in configs:
        elapsed = time.perf_counter() - started
        if budget_seconds is not None and elapsed >= budget_seconds:
            outcomes.append(
                SweepOutcome(
                    atom_names=config.atom_names,
                    max_size=config.max_size,
                    conj_normal=config.conj_normal,
                    certify=config.certify,
                    fingerprint_seed=FINGERPRINT_SEED,
                    status="skipped_budget",
                )
            )
            continue
        outcomes.append(run_one(config))
    return outcomes


def outcomes_to_json(
    outcomes: list[SweepOutcome],
    environment_note: str,
    budget_seconds: float | None = None,
) -> str:
    payload = {
        "environment_note": environment_note,
        "budget_seconds": budget_seconds,
        "outcomes": [asdict(o) for o in outcomes],
    }
    return json.dumps(payload, indent=2, sort_keys=True)
