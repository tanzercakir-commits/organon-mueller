"""The discovery pipeline v1.1 (stage 3):

    enumerate -> FINGERPRINT-bucket -> per-pair ISOLATED e-graph proof
              -> independent multi-seed numeric verification

Classification of a candidate pair (anchor, other) in one fingerprint bucket:

    provable & true    -> verified                 (the harvest)
    provable & false   -> refuted                  (ALARM: unsound axiom; breaks build, K10)
    unprovable & true  -> underivable              (FINDING: novelty / missing-axiom seed, M16)
    unprovable & false -> fingerprint collision    (expected noise, counted)

WHY ISOLATED PROOF GRAPHS (decision M18, stage 3): saturating one large
shared e-graph over the full enumeration produced inconsistent check/extract
results in egglog 13.2.0 — a term's extracted representative could land in a
class with a different atom multiset, and pairs provable in isolation became
"unprovable" in the large graph (see docs/egglog-large-graph-pathology.md
and spikes/egglog_pathology_probe.py for the reproduction).  The engine
therefore builds a FRESH two-term e-graph per candidate pair and saturates
that; isolated graphs behaved correctly in every probe.  This costs little
(pair closures are tiny) and removes the unreliable component entirely.
Soundness never rested on the e-graph alone (M10): the final word is always
the independent numeric verification.

`sound` remains "refuted is empty" — the engine can under-derive, it can
never over-claim (rule K13).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from egglog import EGraph, eq
from egglog.bindings import EggSmolError

from .axioms import structural_rules, to_egglog
from .fingerprint import bucket_by_fingerprint
from .interpret import terms_numerically_equal
from .terms import Term, enumerate_terms

__all__ = ["DiscoveryEngine", "DiscoveryResult", "CandidatePair"]


@dataclass(frozen=True)
class CandidatePair:
    left: Term
    right: Term

    def render(self) -> str:
        return f"{self.left.render()}  ==  {self.right.render()}"


@dataclass
class DiscoveryResult:
    atom_names: tuple[str, ...]
    max_size: int
    conj_normal: bool
    n_terms: int
    n_buckets: int
    verified: list[CandidatePair] = field(default_factory=list)
    refuted: list[CandidatePair] = field(default_factory=list)
    #: numerically true but not derivable from the current axioms — the
    #: novelty / missing-axiom signal (M16). Never counted as verified.
    underivable: list[CandidatePair] = field(default_factory=list)
    fingerprint_collisions: int = 0
    harvest_seconds: float = 0.0

    @property
    def sound(self) -> bool:
        """True iff the e-graph never proved something numerically false."""
        return not self.refuted


class DiscoveryEngine:
    """Hybrid equality-saturation discovery over the abstract Z-algebra."""

    def __init__(
        self,
        atom_names: tuple[str, ...] = ("a", "b"),
        max_size: int = 7,
        conj_normal: bool = False,
    ):
        self.atom_names = atom_names
        self.max_size = max_size
        self.conj_normal = conj_normal
        self.rules = structural_rules(atom_names)

    # -- proof (isolated per pair, decision M18) --------------------------------
    def provable(self, a: Term, b: Term) -> bool:
        """Derivability of a == b from the structural axioms, proven on a
        fresh two-term e-graph (see module docstring for why isolated)."""
        egraph = EGraph()
        egraph.register(to_egglog(a))
        egraph.register(to_egglog(b))
        egraph.run(self.rules.saturate())
        try:
            egraph.check(eq(to_egglog(a)).to(to_egglog(b)))
            return True
        except EggSmolError:
            # a failed proof — anything else (operational failure) propagates,
            # so it can never masquerade as non-equivalence (reviewer, stage 2)
            return False

    # -- full pipeline -----------------------------------------------------------
    def run(self) -> DiscoveryResult:
        terms = enumerate_terms(self.atom_names, self.max_size, self.conj_normal)

        start = time.perf_counter()
        buckets = bucket_by_fingerprint(terms, self.atom_names)
        result = DiscoveryResult(
            atom_names=self.atom_names,
            max_size=self.max_size,
            conj_normal=self.conj_normal,
            n_terms=len(terms),
            n_buckets=len(buckets),
        )
        # Work queue so that fingerprint collisions cannot SHADOW true pairs
        # (stage-3 review): terms that fail both proof and numeric equality
        # against the anchor form a leftover group that is re-examined among
        # itself, recursively. With zero collisions this reduces to one star
        # per bucket.
        queue: list[list[Term]] = [g for g in buckets if len(g) >= 2]
        while queue:
            group = queue.pop()
            anchor = min(group, key=lambda t: (t.size(), t.render()))
            leftovers: list[Term] = []
            for other in group:
                if other is anchor:
                    continue
                pair = CandidatePair(anchor, other)
                provable = self.provable(anchor, other)
                true = terms_numerically_equal(anchor, other, self.atom_names)
                if provable and true:
                    result.verified.append(pair)
                elif provable and not true:
                    result.refuted.append(pair)  # K10: surfaced, never dropped
                elif true:
                    result.underivable.append(pair)  # M16: first-class finding
                else:
                    result.fingerprint_collisions += 1
                    leftovers.append(other)
            if len(leftovers) >= 2:
                queue.append(leftovers)
        result.harvest_seconds = time.perf_counter() - start
        return result
