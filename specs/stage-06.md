# STAGE 6 — New-Candidate Sweep #1 + Novelty Protocol (Phase B)

**Date**: 2026-07-13 · **Previous**: stage-05 (recovery, boundary map)
**Mode**: autonomous

---

## 1. Context

The engine now recovers the known; next is the first systematic NEW-candidate sweep.
The current fragment (atoms+mul+conj) is narrow; this sweep has two legitimate outcomes:
(a) underivable candidates come out → they enter the novelty protocol; (b) the channel comes
out empty → the observation "the axiom set for this fragment appears empirically COMPLETE"
— this too is a reportable result (negative-result discipline). A "novel" claim is never
generated automatically; the comparison only FLAGS candidates.

## 2. Goals

1. **`discovery/sweep.py`**: configured sweep campaign —
   `SweepConfig(atom_names, max_size, conj_normal, certify)` →
   `SweepOutcome` (numbers + underivable rendered pairs + times);
   JSON serialization (persistent evidence artifact `reports/sweep-01-results.json`).
2. **Sweep #1 scope** (according to the measured sizes; with the K15 environment note):
   2-atom pruned-10 (4036 terms) + 3-atom pruned-9 (8331 terms);
   if the time budget permits, a time-boxed attempt at 2-atom pruned-11 (11284).
3. **`docs/novelty-protocol.md`**: the underivable → candidate → claim chain:
   exact symbolic proof (already M19) → canonical presentation → library
   comparison → literature checklist (Gil 2007/2014, Cloude 1986,
   Ossikovski line, Kuntman corpus) → expert (Kuntman) gate. The protocol
   does not generate a CLAIM; the physics-interpretation threshold (critical-decision) is
   preserved.
4. **`docs/design-note-addition-scalars.md`**: input to the Stage 7 spec —
   Sum node + opaque scalar coefficients (hybrid boundary M10: scalar arithmetic
   in SymPy; structural axioms in the e-graph), the fingerprint's transition to a
   scale-relative key, management of the enumeration explosion (initially 2-sum),
   acceptance targets (I15 expansion, I16 interference).

## 3. Architectural decisions

- **M24. The negative result is first-class**: an empty underivable channel is recorded not
  as "failure" but as a fragment-completeness observation, as a JSON artifact +
  in the report.
- **M25. Sweep artifacts in the repo**: the summary of each sweep campaign is
  `reports/sweep-NN-results.json` (deterministic, reproducible
  with the configuration).

## 4. Strict rules

- K21. The sweep configurations and seeds are embedded in the artifact (reproducibility).
- K22. CI tests are limited to a small configuration (the full sweep does not run in CI);
  the full sweep results are verified from the artifact.

## 5-6. Deliverable + Verification

`discovery/sweep.py` · `tests/test_sweep.py` (small config, determinism,
JSON round-trip, field integrity) · `reports/sweep-01-results.json` ·
`docs/novelty-protocol.md` · `docs/design-note-addition-scalars.md` · report.
Suite green; sweep results as a table in the report.

## 7-9.

Push + report + Stage 7 (5 min). Warning: at deep sizes the per-pair proof time
grows with the term size — the budget is checked BETWEEN configs (a started config
completes, it may overrun; no mid-run cutoff); when the budget runs out the remaining
configs are recorded with `skipped_budget` + null observation fields. Out of scope:
the implementation of the expansion (Stage 7), Lean, MCP.

**STOP HERE**
