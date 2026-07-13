"""The discovery pipeline v1.2 (stages 3-4):

    enumerate -> FINGERPRINT-bucket -> per-pair ISOLATED e-graph proof
              -> independent multi-seed numeric verification
              -> symbolic-EXACT certification (certify mode, stage 4 / M19)

Classification of a candidate pair (anchor, other) in one fingerprint bucket
(sym = exact symbolic proof, consulted per the certify mode):

    provable & numeric-true                  -> verified  (certify="all" also demands sym;
                                                           sym failure there -> refuted, loudest alarm)
    provable & numeric-false & sym-true      -> verified + numeric_false_negatives += 1
                                                (numeric-layer jitter rescued by layer 1)
    provable & numeric-false & sym-false     -> refuted   (ALARM: unsound axiom; breaks build, K10)
    unprovable & numeric-true & sym-true     -> underivable (FINDING: novelty seed, M16/M19)
    unprovable & numeric-true & sym-false    -> demoted_by_symbolic (sampling coincidence, K16)
    unprovable & numeric-false               -> fingerprint collision (expected noise, counted)

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
from .symbolic import terms_symbolically_equal
from .terms import Term, enumerate_terms

__all__ = [
    "DiscoveryEngine",
    "DiscoveryResult",
    "CandidatePair",
    "DiscoveryInvariantError",
]


class DiscoveryInvariantError(AssertionError):
    """A runtime invariant of the discovery result was violated (M20)."""


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
    #: numerically true AND symbolically certified (default certify mode),
    #: but not derivable from the current axioms — the novelty /
    #: missing-axiom signal (M16/M19). Never counted as verified.
    underivable: list[CandidatePair] = field(default_factory=list)
    #: numerically true but the EXACT symbolic proof failed — a sampling
    #: coincidence caught by layer 1 (K16: surfaced, never silently dropped).
    demoted_by_symbolic: list[CandidatePair] = field(default_factory=list)
    fingerprint_collisions: int = 0
    #: provable + symbolically exact but numeric sampling said false —
    #: a numeric-layer false negative rescued by layer 1 (stage-4 review).
    numeric_false_negatives: int = 0
    certify: str = "underivable"
    harvest_seconds: float = 0.0

    @property
    def sound(self) -> bool:
        """True iff no proof was contradicted by the strongest available
        verification layer (numeric, or symbolic-exact under certify)."""
        return not self.refuted

    def check_invariants(self) -> None:
        """Runtime guards (M20, user directive 2026-07-13). Raises on violation."""
        buckets_pairs = [
            ("verified", self.verified),
            ("refuted", self.refuted),
            ("underivable", self.underivable),
            ("demoted_by_symbolic", self.demoted_by_symbolic),
        ]
        seen: dict = {}
        for name, pairs in buckets_pairs:
            for p in pairs:
                key = frozenset((p.left, p.right))
                if key in seen:
                    where = (
                        f"twice in {name}" if seen[key] == name
                        else f"in two categories: {seen[key]} and {name}"
                    )
                    raise DiscoveryInvariantError(f"pair {where}: {p.render()}")
                seen[key] = name
                if p.left == p.right:
                    raise DiscoveryInvariantError(f"degenerate pair: {p.render()}")
        # accounting holds even with collisions (stage-4 review): every
        # examined pair lands in exactly one category or the collision counter
        categorized = sum(len(pairs) for _, pairs in buckets_pairs)
        examined = categorized + self.fingerprint_collisions
        expected = self.n_terms - self.n_buckets
        if self.fingerprint_collisions == 0 and categorized != expected:
            raise DiscoveryInvariantError(
                f"pair accounting broken: categorized {categorized} != "
                f"n_terms - n_buckets = {expected}"
            )
        if examined < expected:
            raise DiscoveryInvariantError(
                f"pairs lost: examined {examined} < minimum {expected}"
            )
        if self.fingerprint_collisions < 0 or not (self.harvest_seconds >= 0):
            raise DiscoveryInvariantError("negative or NaN counter")
        if self.numeric_false_negatives < 0:
            raise DiscoveryInvariantError("negative counter")
        if self.certify not in {"none", "underivable", "all"}:
            raise DiscoveryInvariantError(f"unknown certify mode: {self.certify}")


class DiscoveryEngine:
    """Hybrid equality-saturation discovery over the abstract Z-algebra."""

    def __init__(
        self,
        atom_names: tuple[str, ...] = ("a", "b"),
        max_size: int = 7,
        conj_normal: bool = False,
        certify: str = "underivable",
    ):
        if certify not in {"none", "underivable", "all"}:
            raise ValueError(f"unknown certify mode: {certify}")
        if len(set(atom_names)) != len(atom_names):
            raise ValueError(f"duplicate atom names: {atom_names}")
        self.atom_names = atom_names
        self.max_size = max_size
        self.conj_normal = conj_normal
        self.certify = certify
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
            certify=self.certify,
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
                    if self.certify == "all" and not terms_symbolically_equal(
                        anchor, other, self.atom_names
                    ):
                        # e-graph AND numeric sampling both wrong: loudest alarm
                        result.refuted.append(pair)
                    else:
                        result.verified.append(pair)
                elif provable and not true:
                    # before raising the unsoundness alarm, consult the exact
                    # layer (stage-4 review): provable + symbolically TRUE +
                    # numerically false is a numeric-layer false negative
                    # (tolerance jitter), not an unsound axiom
                    if self.certify in {"underivable", "all"} and (
                        terms_symbolically_equal(anchor, other, self.atom_names)
                    ):
                        result.verified.append(pair)
                        result.numeric_false_negatives += 1
                    else:
                        result.refuted.append(pair)  # K10: surfaced, never dropped
                elif true:
                    if self.certify in {"underivable", "all"} and not (
                        terms_symbolically_equal(anchor, other, self.atom_names)
                    ):
                        # numeric sampling coincidence, caught by layer 1 (K16)
                        result.demoted_by_symbolic.append(pair)
                    else:
                        result.underivable.append(pair)  # M16/M19: finding
                else:
                    result.fingerprint_collisions += 1
                    leftovers.append(other)
            if len(leftovers) >= 2:
                queue.append(leftovers)
        result.harvest_seconds = time.perf_counter() - start
        result.check_invariants()  # M20: runtime guards, not just tests
        return result
