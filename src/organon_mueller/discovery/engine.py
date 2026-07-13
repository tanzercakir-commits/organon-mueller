"""The discovery pipeline: enumerate -> saturate -> harvest -> verify.

Contract (rules K9/K10): the engine never reports an unverified pair, and a
verification FAILURE is not silently dropped — it is surfaced in the result
(`refuted`) because it signals an unsound axiom, which must fail the build.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from egglog import EGraph, eq
from egglog.bindings import EggSmolError

from .axioms import structural_rules, to_egglog
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
    n_terms: int
    n_classes: int
    verified: list[CandidatePair] = field(default_factory=list)
    refuted: list[CandidatePair] = field(default_factory=list)
    saturation_seconds: float = 0.0
    #: defensive splits in _bucket_by_class (extraction-representative
    #: collisions). Nonzero means possible completeness loss — never
    #: soundness loss — and should be investigated.
    extraction_collisions: int = 0

    @property
    def sound(self) -> bool:
        """True iff every harvested candidate survived numeric verification."""
        return not self.refuted


class DiscoveryEngine:
    """Hybrid equality-saturation discovery over the abstract Z-algebra."""

    def __init__(self, atom_names: tuple[str, ...] = ("a", "b"), max_size: int = 7):
        self.atom_names = atom_names
        self.max_size = max_size
        self.rules = structural_rules(atom_names)

    # -- e-graph construction -------------------------------------------------
    def saturate(self, terms: list[Term]) -> tuple[EGraph, float]:
        egraph = EGraph()
        for term in terms:
            egraph.register(to_egglog(term))
        start = time.perf_counter()
        egraph.run(self.rules.saturate())
        return egraph, time.perf_counter() - start

    @staticmethod
    def equivalent(egraph: EGraph, a: Term, b: Term) -> bool:
        try:
            egraph.check(eq(to_egglog(a)).to(to_egglog(b)))
            return True
        except EggSmolError:
            # a failed proof — anything else (operational failure) propagates,
            # so it can never masquerade as non-equivalence (reviewer, stage 2)
            return False

    # -- harvest ---------------------------------------------------------------
    def _bucket_by_class(
        self, egraph: EGraph, terms: list[Term]
    ) -> tuple[list[list[Term]], int]:
        """Group terms into e-classes.

        Primary key: the extracted canonical representative (decision M12);
        extraction is only trusted WITHIN this EGraph instance.  Buckets are
        then confirmed pairwise-adjacent with `check`, so a representative
        collision cannot silently merge distinct classes.
        """
        buckets: dict[str, list[Term]] = {}
        for term in terms:
            rep = str(egraph.extract(to_egglog(term)))
            buckets.setdefault(rep, []).append(term)
        confirmed: list[list[Term]] = []
        collisions = 0
        for group in buckets.values():
            anchor = group[0]
            same = [anchor]
            for other in group[1:]:
                if self.equivalent(egraph, anchor, other):
                    same.append(other)
                else:  # extraction collision: split defensively
                    collisions += 1
                    confirmed.append([other])
            confirmed.append(same)
        return confirmed, collisions

    # -- full pipeline -----------------------------------------------------------
    def run(self) -> DiscoveryResult:
        terms = enumerate_terms(self.atom_names, self.max_size)
        egraph, elapsed = self.saturate(terms)
        classes, collisions = self._bucket_by_class(egraph, terms)

        result = DiscoveryResult(
            atom_names=self.atom_names,
            max_size=self.max_size,
            n_terms=len(terms),
            n_classes=len(classes),
            saturation_seconds=elapsed,
            extraction_collisions=collisions,
        )
        for group in classes:
            if len(group) < 2:
                continue
            anchor = min(group, key=lambda t: (t.size(), t.render()))
            for other in group:
                if other is anchor:
                    continue
                pair = CandidatePair(anchor, other)
                if terms_numerically_equal(anchor, other, self.atom_names):
                    result.verified.append(pair)
                else:
                    result.refuted.append(pair)  # K10: surfaced, never dropped
        return result
