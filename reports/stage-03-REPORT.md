# STAGE 3 — REPORT

**Date**: 2026-07-13 · **Spec**: `specs/stage-03.md` · **Mode**: autonomous
**Result**: COMPLETED — 65/65 tests green; pipeline v1.1; **a significant
reliability finding was caught and worked around** (below).

---

## 1. Deliverables

- **Pipeline v1.1 (reversed flow)**: numerical fingerprint buckets SUGGEST candidates
  (`fingerprint.py`, coarse 3-decimal key, seed independent of verification) →
  each candidate pair is PROVEN in an **isolated two-term e-graph** → independent
  multi-seed numerical verification decides. New class: **`underivable`** —
  a pair that is numerically correct but underivable from the axioms (a novelty/missing-axiom
  signal; input to Stages 5-6).
- **conj-normal pruned enumeration** (`terms.py`): Conj only at the atom
  level; at size 9, 5698 → 1476 terms. (Content is preserved modulo the max_size shift
  margin — an honest record in the docstring.)
- Collision-shadowing closure: the residue of a bucket that experiences a fingerprint collision
  is re-examined among itself (completeness loss closed).
- `spikes/bench_stage3.py`, `spikes/egglog_pathology_probe.py`,
  `docs/egglog-large-graph-pathology.md`.

## 2. RELIABILITY FINDING — egglog 13.2.0 large-graph pathology

On a single shared e-graph (1476 terms), saturation came out **inconsistent**:
9 pairs proven in isolation appeared "unprovable" in the large graph; `extract`
dropped a term into a class with a **different atom multiset** (no axiom
can change the multiset — an impossible representative). The auditor pinned the root cause into the
library with three independent arguments (monotonicity violation, congruence
violation, multiset invariant) and reproduced all the numbers.

**Caught by design**: the e-graph was never the sole verifier
(M10); when the false-underivable pairs appeared in the numerical layer as "correct but
unproven" they raised an alarm. **Resolution (M18)**: the shared graph was removed;
each pair is proven in a fresh two-term graph. Deliberate trade-off: reliability instead of speed.
Since reporting a bug upstream is external contact, it was left to user
approval (critical-decision list).

## 3. Measurements (this sandbox; K15)

| mode | size | terms | buckets | verified | underivable | refuted | collision | time |
|---|---|---|---|---|---|---|---|---|
| full | 7 | 570 | 64 | 506 | 0 | 0 | 0 | ~10 s |
| pruned | 7 | 212 | 56 | 156 | 0 | 0 | 0 | ~3 s |
| pruned | 9 | 1476 | 128 | **1348** | **0** | **0** | 0 | ~30 s |

Internal-consistency invariant in test: when collision=0, verified = terms − buckets.

## 4. Independent audit

Verdict: **PASS**. It reproduced the pathology probes; independently verified the rule-by-rule multiset
preservation; measured the fingerprint's −0.0 normalization and
the false-separation distance (nearest boundary 1.3e-7 — 5 orders of magnitude away from the 1e-12
jitter). Three of its suggestions were applied: collision-shadowing closure, a pathology
family regression (6 pairs) + the verified=terms−buckets invariant, docstring/K14/spec
corrections.

## 5. Next stage (autonomous continuation)

**Stage 4 — Candidate pipeline: numerical pre-sieve → symbolic proof**: a SymPy **symbolic-exact**
verification layer for the underivable pairs (an exact proof instead of random sampling, binding
VERIFICATION.md layer-1 to the discovery side) + an atom-count scaling
(3 atoms) attempt.
