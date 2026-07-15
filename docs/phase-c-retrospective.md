# Phase C Retrospective (A8–A11) — stage-11

v1 iter convention; the Phase B retrospective was in the stage-07 report, but
Phase C's is a standalone document (the decomposition layer has become a
permanent subsystem).

## 1. What was built

The `decomposition/` package in four steps: deriver (A8: Table 2, 6/6
symbolic one-to-one) → composite types (A9: Table 4, 3/3) → rank-3
(A10: beyond-the-paper, M34 framework) → bridge + scores (A10-11). Alongside
it, the first half of guarded-atoms (A9) gave the first non-empty output of
the `underivable` channel.

## 2. Decision/rule consistency scan (M28–M34, K26–K32)

- **M28 (equations are derived, not copied)** — preserved in all three
  stages; even in rank-3, where the anchor itself is absent, the derivation
  discipline did not change.
- **M29 (basis separation)** / **M30 (OCR unreliability — overline losses
  in anchor entries are documented with rationale)** / **M31 (composite is a
  separate module)** / **M33 (one-way layering)** — the file structure
  conforms exactly to these boundaries; rank3 only calls solve's PUBLIC
  decompose; the M30 discipline operated in the Table-2/4 anchor notes and in
  two typo diagnoses.
- **M32 (Horn ruling format)** — the four-part evidence record is in
  `GuardedFinding`; the guard-free-false control is mandatory and tested.
- **M34 (paper-anchor substitution)** — the three layers (probe-backed hand
  derivation + deriver one-to-one match + independent auditor derivation)
  operated fully in A10; the auditor independently verified five formulas and
  the denominator interpretations.
- **K26 (no silent errors)** — trace-1, finiteness, denominator, domain,
  PSD/rank-1, consistency (K32) guards in all three solvers; even "rejection
  for the WRONG REASON" was counted as a defect and fixed (the center-only
  boundary family).
- **K28 anchor discipline** — Table 2/4 anchors entered by hand and in
  SEPARATE test files; in rank-3, M34 was used deliberately instead of K28.
- **K27 (deterministic seeds)** — all sweep/campaign/roundtrip tests are
  fixed-seed (20260713, 424242; the K32 family is 0); artifacts carry the
  seeds (together with K21).
- **K29/K31 (structural minor guards)** — thrown at derivation time; the
  solve-order sensitivity (K31) is rank-3's new contribution.
- **K30 (by constraint-construction, no assumption-injection)** — guarded
  generators are constrained by parametrization; there is no sympy assumption
  injection; the fidelity meta-test (stage-11) structuralized this.
- **K32 (over-determination mandatory check)** — the auditor's MAJOR got its
  own regression test (the all-real family, seed 0).

## 3. Technical debt inventory

| Debt | Status | Rationale/window |
|---|---|---|
| rank-3 a/b minor variants (M33 note) | DEFERRED | the variant denominators separate only in measure-zero degenerations (u₁=0 vs u₂=0); noisy real data does not settle on these points; opens up when experimental data arrives |
| bridge v1 pre-ranking | CLOSED (stage-11) | `ProposeReport.scores`, denominator-health score; only ranks |
| guard-generator fidelity (design-note O1) | STRUCTURALIZED (stage-11) | GUARD_KEYS↔generator meta-test; a new key cannot enter without a generator |
| interpreted_scalars denominator side-conditions (O2) | CONDITIONAL DEBT | the feature is not in the language (K19); a mandatory acceptance item at the stage it enters the language |
| guarded-atoms 2nd half (unitary/hermitian campaigns) | OPEN | between Phase D-E; currently limited to the generator+fidelity test (honest scope) |
| stage-10 auditor suggestions | CLOSED (stage-10) | primary="center" construction, finiteness, K32/u₀=u₃/cross-pair tests, zero-matrix guard |

## 4. Lessons

1. **Probe-before-spec paid off twice**: a wrong unitary target (A9) was
   eliminated before touching code; a type-3 edge sign error (A10) was caught
   before entering the spec. The rule is now part of the execution chain.
2. **The rule to not pipe pytest was violated once** (within A10, with tail) —
   the output masked the exit; it was noticed in the same round and rerun
   bare. The rule reminder stays in the project document.
3. **The assumption "a negative control must be rejected" was wrong**: in
   rank-3 the accepted alternative was a VALID output (non-uniqueness). The
   correct framing is "accept → verify": the sweep now separately verifies the
   accepted alternatives too. Lesson: honesty is in verifying, not in
   rejecting.
4. **The auditor layer produces theorems**: the reshuffle identity (A8), the
   {2,3} within-hypothesis uniqueness proof (A10) came out of the audit —
   layer 5 does not just find errors, it strengthens the mathematics.

## 5. Handoff to Phase D

Ready ground for the coupled-dipole module (A12-15): HVector/quaternion
representations, discovery engine + guarded atoms (dimer symmetries are
natural guard candidates), decomposition solvers (type analysis of dimer
covariances), novelty protocol. Feedback from the Kuntman package may change
Phase D's internal order (per FROZEN-22 the count/scope does not change).
