# STAGE 3 — Enumeration Scaling + Harvest Pipeline v1 (Phase B)

**Date**: 2026-07-13 · **Previous**: stage-02 (engine v0, FROZEN-22)
**Mode**: autonomous (mandate 2026-07-13)

---

## 1. Context

The bottleneck of the v0 harvest is `extract` (~21 s at size 9; saturation 0.15 s).
Also, v0 was harvesting equivalences that the e-graph ALREADY proved — it had no ability to
see "numerically correct but not derivable from the axioms" pairs. Yet the real target of
Phase B is exactly that gap: a correct equivalence that is not derivable = potential new
identity / missing-axiom signal.

## 2. Goals

1. **Pipeline v1 (reverse flow)**: numerical fingerprint GENERATES candidate → e-graph
   PROVES derivability → independent multi-seed numerical verification CONFIRMS.
   Classification:
   - `verified`: proven + verified
   - `refuted`: proven but numerically wrong (ALARM — unsound axiom, breaks the build)
   - `underivable`: numerically correct but not derivable from the axioms (FINDING —
     novelty/missing-axiom seed; input to Stages 5-6)
   - `fingerprint_collisions`: coarse-key collision, dropped in the numerical elimination (normal)
2. **conj-normal (pruned) enumeration**: Conj only at the atom level —
   the conj(conj(x)) and conj(x·y) forms are dropped from generation (e-graph fodder is
   reduced); identity content is preserved in normal form.
3. **Measurement**: size 7/8/9, pruned/unpruned: number of terms, saturation, harvest times
   — table in the report.
4. The extract-based `_bucket_by_class` is removed in v1 (together with the
   `extraction_collisions` field); the check-based acceptance tests (R1-R3, negatives) are
   kept exactly as-is.

## 3. Architectural decisions

- **M18 (added during implementation). Proofs in an isolated pair-graph**:
  the shared large e-graph showed inconsistent check/extract behavior in egglog 13.2.0
  (an extract representative falling into a different atom-multiset; a pair proven in
  isolation not being provable in the large graph — repro:
  `spikes/egglog_pathology_probe.py`, analysis:
  `docs/egglog-large-graph-pathology.md`). In v1.1 each candidate pair is saturated and
  checked in its own fresh two-term graph; the shared graph is removed.
  Soundness already rested on numerical verification (M10); that layer also caught the
  pathology.

- **M15. Fingerprint = candidate generator, NEVER proof**: the coarse key (single fixed
  assignment, rounding to 3 decimals) is only for chasing. False-merge → later layers
  eliminate it; false-split (boundary jitter, ~1e-4-close rounding boundary) → only loss of
  completeness. The soundness guarantee rests on the fingerprint at no point.
- **M16. `underivable` first-class output**: it is not silently swallowed, it is counted and
  reported; it is NOT INCLUDED in the definition of `sound` (sound = refuted empty).
- **M17. The discovery API may evolve throughout Phase B** (v0→v1); it is frozen in Stage 7.
  The Stage 0-1 APIs (K11) do not change.

## 4. Strict rules

- K13. `verified` is only the intersection of proof+verification; `underivable` is never
  presented as "discovery" in any counter, it is reported separately.
- K14. The fingerprint assignment and the verification seeds are DIFFERENT (independence).
- K15. Benchmark numbers go into the report with a note of the environment they were measured
  in.

## 5. Deliverable

- `discovery/fingerprint.py`, `engine.py` v1, `terms.py` (conj_normal parameter)
- `tests/test_discovery.py` updated (new classification + pruned-enumeration feature tests +
  the conj-normal counterpart of R3 appearing in the harvest)
- `spikes/bench_stage3.py` + report table
- `reports/stage-03-REPORT.md`

## 6. Verification

- R1-R3 tests (in isolated pair-graphs per M18) green exactly as-is.
- v1 full run (conj-normal, size 9): the R2 pair and the conj-normal form of R3
  ((a·b)·(conj(a)·conj(b)) ≡ (a·conj(a))·(b·conj(b))) are within `verified`.
- `refuted` empty; `underivable` expected in this fragment: empty (if not, a pre-review is
  done, the finding is written into the report; the stage can also pass while it is
  non-empty — K13).
- Harvest: measured (this environment, v1.1 isolated proofs) — pruned size 9:
  1476 terms, 128 buckets, 1348 verified, 0 underivable/refuted, ~30 s (including full
  classification; v0's 21 s extract was only grouping and had no underivable view).
  The "<5 s" target in the first draft was for the chasing that replaces v0's extract; in
  v1.1 the time goes to the proof calls — a deliberate trade-off: reliability instead of
  speed.

## 7-9. Delivery format / Warnings / Out of scope

Push + report + Stage 4 planning. Warning: absolute rounding (3 decimals) in the fingerprint
key is sufficient for magnitude ~10 values; once scalar coefficients arrive (later in Phase B)
we will switch to a scale-relative key. Out of scope: scalar terms, canonical-form cost
function, literature comparison.

**STOP HERE**
