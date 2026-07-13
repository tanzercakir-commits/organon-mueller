"""Numeric fingerprint bucketing — the candidate PROPOSER of pipeline v1.

A fingerprint is a coarse hash of a term's value on ONE fixed random
assignment: every matrix entry rounded to 3 decimals (decision M15).

Guarantees and non-guarantees:

* A fingerprint is NEVER a proof.  False merges (distinct terms colliding)
  are filtered downstream by the e-graph check and the rigorous multi-seed
  numeric verification.  False splits (truly equal terms rounding across a
  boundary because of ~1e-12 float jitter) are possible in principle but
  need an entry within ~1e-12 of a 0.0005 grid line — astronomically rare
  for continuous random draws, deterministic under the fixed seed, and cost
  only completeness, never soundness.
* The fingerprint assignment seed is deliberately DIFFERENT from the
  verification seeds (rule K14).
"""
from __future__ import annotations

import numpy as np

from .interpret import evaluate, random_assignment
from .terms import Term

__all__ = ["fingerprint_key", "bucket_by_fingerprint", "FINGERPRINT_SEED"]

FINGERPRINT_SEED = 424242  # distinct from verification seeds (K14)
_DECIMALS = 3


def fingerprint_key(term: Term, assignment: dict[str, np.ndarray]) -> bytes:
    value = evaluate(term, assignment)
    quantized = np.round(value, _DECIMALS) + 0.0  # normalize -0.0 to +0.0
    return quantized.tobytes()


def bucket_by_fingerprint(
    terms: list[Term],
    atom_names: tuple[str, ...],
    seed: int = FINGERPRINT_SEED,
) -> list[list[Term]]:
    """Group terms by coarse numeric fingerprint (candidate classes)."""
    rng = np.random.default_rng(seed)
    assignment = random_assignment(atom_names, rng)
    buckets: dict[bytes, list[Term]] = {}
    for term in terms:
        buckets.setdefault(fingerprint_key(term, assignment), []).append(term)
    return list(buckets.values())
