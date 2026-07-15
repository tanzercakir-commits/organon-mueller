# STAGE 4 — REPORT

**Date**: 2026-07-13 · **Spec**: `specs/stage-04.md` · **Mode**: autonomous
**Result**: COMPLETED — 75/75 tests green; the symbolic-exact layer was bound to discovery;
runtime guards in production code (the code counterpart of the user directive).

---

## 1. Deliverables

- **`discovery/symbolic.py` (layer-1 discovery binding, M19)**: abstract term →
  per-atom independent generic-parameter symbolic Z-matrix; `expand`-based
  **EXACT** equality proof (a theorem, not a sample). The auditor proved that the procedure is both
  sound and complete for this term language (a z/z̄
  polarization argument) and verified that in a 66-term pool the proof≡symbolic layers
  coincide one-to-one (68/68 pairs).
- **Certification modes** `certify ∈ {none, underivable, all}` (default
  `underivable`): every pair entering the publication-candidate `underivable` channel now has an
  exact proof; one that fails to pass drops to `demoted_by_symbolic` (K16, transparent).
  `certify="all"`: verified pairs are also certified. New recovery path:
  proven + symbolic-correct + numerically-wrong → taken into verified as a numerical-layer
  false-negative (jitter) and counted (a misleading alarm is prevented).
- **Runtime invariant guards (M20)**: `DiscoveryResult.check_invariants()`
  is called by the engine at the end of each run — category disjointness, pair
  accounting (missing-pair check even in the collision case), NaN/negative counter,
  degenerate pair. It is tested that the guard actually fires with a deliberately corrupted
  result. Atom name uniqueness is verified in the constructor.
- **Property-based tests (hypothesis, derandomize — K2/K18)**: P1
  proof⇒numerical (the soundness contract), P2 symbolic⇒numerical (layer consistency),
  P3 enumeration determinism. The auditor measured that in the first version the antecedents almost
  never fired (4.6% base rate) → a constructed-equal-pair generator was
  added; now **13/30 nontrivial hits** in each deterministic run.
- **3-atom scaling** (this sandbox): pruned-7 → 825 terms / 630 verified /
  18.5 s; pruned-8 → 2499 / 2196 / 68 s; all with 0 underivable/demoted/refuted.
  2-atom pruned-7 `certify="all"`: 156/156 certified, ~13 s.
- Pathology document updated: the user decision (no upstream report) +
  **eliminated hypotheses** — memory management (proof pattern does not match) and
  the `seminaive` flag (same behavior in both settings; tested upon the user's question).

## 2. Independent audit

Verdict: **PASS**. The symbolic layer's proof-value was formally justified;
the classification paths and the collision-queue withstood targeted corruption attempts
(a 5-term bucket, in a 4-round cascade each pair was examined exactly once); all
benchmark numbers were independently reproduced. All three of its suggestions were applied:
the property-test generator, the numerical-false-negative recovery path, guard
tightening (+ docstring updates).

## 3. Decisions

- Per M19, every output that could carry a "new identity" claim henceforth passes through the
  exact-proof layer; no numerical-only result can enter the finding channel.
- 3-atom scaling is 68 s on pruned-8 — acceptable for beyond Phase B;
  deeper sweeps (Stage 6) are a bucket-parallelization candidate (noted).

## 4. Next stage (autonomous continuation)

**Stage 5 — Recovery campaign**: the engine must rediscover on its own the subset of I1–I21 in the
library that is translatable into the term language; the untranslatable ones
(those requiring scalar coefficients/Stokes) are listed explicitly → the requirement list for
the post-Phase-B term language expansion emerges from this gap.
