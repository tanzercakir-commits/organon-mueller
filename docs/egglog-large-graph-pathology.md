# egglog 13.2.0 Large-Graph Pathology (Stage 3 finding)

**Date**: 2026-07-13 · **egglog-python**: 13.2.0 · **Status**: worked around
with engine v1.1 (decision M18); root cause is not ours (library) — to be tracked.

## Observation

Saturating the full enumeration (conj-normal, size 9, 1476 terms) in a SINGLE
shared e-graph produced inconsistent results:

1. `b·(a·conj(a)) == b·(conj(a)·a)` — PROVEN in an isolated two-term graph
   (associativity + atom commutation); in the 1476-term graph the `check`
   FAILS, and 30 extra iterations do not fix it. The child classes
   (a·conj(a) ≡ conj(a)·a) are merged while the parents stay separate — an
   appearance contrary to congruence closure.
2. Worse: `extract(b·(conj(a)·a))` yields a representative that **does not
   contain b** (`a·(a·conj(a·a))`) — a class from a different atom multiset.
   Since none of the axioms can change the atom multiset, this is either an
   incorrect merge or a fresh-node insertion/canonicalization error.
3. The same pairs can come out correct in the 5698-term UNPRUNED graph — the
   behavior is sensitive to the registration set and deterministically
   reproducible (`spikes/egglog_pathology_probe.py`).

## Impact and defense

- The engine never trusted the e-graph on its own (decision M10); the final
  word is in independent multi-seed numeric verification. The pathology was
  caught precisely thanks to this layer: the spurious "underivable" pairs
  raised an alarm when they appeared numerically correct but unproven.
- **v1.1 (decision M18)**: the shared large graph was removed; each candidate
  pair is proven in its own fresh two-term e-graph. In isolated mode the
  behavior is consistent across all probes; 9/9 stuck pairs were proven.

## Eliminated hypotheses (2026-07-13, on the user's question)

- **Memory management**: no — the graphs are small (≈10³ nodes), the error is
  deterministic and content-dependent; the larger (5698) graph is correct
  while the smaller one (1476) is faulty — inconsistent with a memory-pressure
  pattern.
- **The `seminaive` flag**: no — the same behavior occurs with
  `EGraph(seminaive=False)` too (tested in both settings). No other relevant
  configuration surface is visible in the API (`RunConfig` is at the
  iteration/scheduler level; extra iterations were already tried).

## Open work

- Reporting upstream — the decision is CURRENT (Jul 13, afternoon): the user
  said "maybe we'll write it up"; **draft ready**: `egglog-upstream-issue-draft.md`
  (single rule + a 1-minimal repro of 29 terms, reduced with delta-debug).
  SUBMISSION still depends on user approval (M23, critical-decision: external
  contact).
- On egglog version upgrades, the probe script must be rerun.
