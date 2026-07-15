# STAGE 4 — Symbolic-Exact Proof Layer + Runtime Guards (Phase B)

**Date**: 2026-07-13 · **Previous**: stage-03 (v1.1, pathology finding, M18)
**Mode**: autonomous · **User directive (2026-07-13)**: "the only insurance against
non-determinism is tests — work as much as possible with tests and guards."

---

## 1. Context

In v1.1 the verdict of "correct" rests on numerical sampling (layer 2). VERIFICATION.md
layer 1 (symbolic-exact) is not yet connected to the discovery side; since the `underivable`
pairs are the publication-candidate finding channel, everything entering that channel must be
EXACTLY proven. Also, per the user directive, the engine's result invariants must now be
checked at runtime as well.

## 2. Goals

1. **`discovery/symbolic.py`**: abstract term → generic-parameterized symbolic
   Z-matrix evaluation; `terms_symbolically_equal` (expand-based EXACT).
2. **Certification mode in the engine** `certify ∈ {"none","underivable","all"}`
   (default `"underivable"`):
   - if an `underivable` candidate cannot pass the symbolic proof → `demoted_by_symbolic`
     (coincidence of the numerical sampling; in a separate list, transparent).
   - when `certify="all"`, if a `verified` pair cannot pass the symbolic proof →
     `refuted` (e-graph + numerical being wrong together = big alarm, breaks the build).
3. **Runtime invariant guards**: `DiscoveryResult.check_invariants()` —
   the categories are disjoint; when collision=0, verified+underivable+refuted+demoted =
   terms−buckets; times ≥0; the engine CALLS it at the end of `run()`, a violation
   raises `DiscoveryInvariantError` (no silent pass).
4. **Property-based tests** (hypothesis, added to the `[test]` extra;
   with `derandomize=True` CI is deterministic — K2 is preserved):
   - P1: `provable(t1,t2) ⇒ terms_numerically_equal` (soundness contract)
   - P2: `terms_symbolically_equal ⇒ terms_numerically_equal` (layer consistency)
   - P3: enumerate determinism + duplicate-free (over random size/atoms)
5. **3-atom scaling measurement**: (a,b,c) pruned size 7 (and size 8 if time permits)
   full run; numbers to the report.
6. Pathology document "Open work" update: upstream notification WILL NOT BE MADE
   (user decision, 2026-07-13).

## 3. Architectural decisions

- **M19. Publication-candidate channel rule**: `underivable` output can only be reported
  after a symbolic-exact proof (the default certify level guarantees this). Numerical-only
  correctness cannot enter any finding channel on its own.
- **M20. Guards in production code**: invariant checking is not test-only, it is in the
  engine itself (the code counterpart of the user directive).
- **M21. hypothesis is a test dependency only**; the core dependencies do not change.

## 4. Strict rules

- K16. `demoted_by_symbolic` is not silently dropped; it is listed in the result.
- K17. Symbolic evaluation uses a SEPARATE generic parameter set per atom
  (sharing = risk of proving a false identity).
- K18. Property tests run with the deterministic profile (derandomize).

## 5. Deliverable

`discovery/symbolic.py` · `engine.py` (certify + guards) ·
`tests/test_symbolic.py` · `tests/test_properties.py` · pyproject ([test] +=
hypothesis) · bench update (3-atom) · pathology doc update ·
`reports/stage-04-REPORT.md`.

## 6. Verification

- The R3 pair also passes with the symbolic-exact proof (proof of the layer-1 discovery link).
- Negative: a·b vs b·a is also NOT symbolically equal.
- pruned-7 full run with `certify="all"`: all verified are symbolically certified,
  demoted empty; time to the report.
- pruned-9 with default certify: the previous numbers are preserved (1348 verified).
- Invariant guard: a `DiscoveryInvariantError` test with a deliberately corrupted fake result.
- Whole suite (including hypothesis) green; 3-atom measurement in the report.

## 7-9. Delivery format / Warnings / Out of scope

Push + report + Stage 5 planning. Warnings: the symbolic matmul chain gets expensive at 4+
atoms — certify is not made the default "all" without measuring the times;
`conjugate()` is element-wise (not dagger). Out of scope: scalar-coefficient
term language, canonical form, literature comparison, Lean.

**STOP HERE**
