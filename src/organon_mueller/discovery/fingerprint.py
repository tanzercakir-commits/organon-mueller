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
_ZERO_KEY = b"ZERO"
_ZERO_EPS = 1e-12


def fingerprint_key(term: Term, assignment) -> bytes:
    """Scale-relative key (stage 7): entries of M / ||M||_F rounded.

    Frobenius normalization keeps the key meaningful when opaque scalars
    make magnitudes arbitrary. Proportional-but-distinct terms may collide
    — expected, and filtered by the proof + verification layers (M15).
    Truly equal terms always share a key (same exact value).
    """
    value = evaluate(term, assignment)
    norm = float(np.linalg.norm(value))
    if not (norm > _ZERO_EPS):
        return _ZERO_KEY
    quantized = np.round(value / norm, _DECIMALS) + 0.0  # -0.0 -> +0.0
    return quantized.tobytes()


def bucket_by_fingerprint(
    terms: list[Term],
    atom_names: tuple[str, ...],
    seed: int = FINGERPRINT_SEED,
    scalar_names: tuple[str, ...] = (),
) -> list[list[Term]]:
    """Group terms by coarse numeric fingerprint (candidate classes)."""
    rng = np.random.default_rng(seed)
    assignment = random_assignment(atom_names, rng, scalar_names)
    buckets: dict[bytes, list[Term]] = {}
    for term in terms:
        buckets.setdefault(fingerprint_key(term, assignment), []).append(term)
    return list(buckets.values())
