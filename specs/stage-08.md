# STAGE 8 — Symmetry-Conditioned Decomposition Deriver v0 (PHASE C opening)

**Date**: 2026-07-13 · **Previous**: stage-07 (Sum/Scale, Phase B closure)
**Mode**: autonomous · **Source**: Kuntman & Arteaga, Appl. Opt. 55, 2543 (2016)
(project file `decompositionofadepolarizingmm.pdf` — read in full in this stage)

---

## 1. Context

Phase C goal: to have the engine itself PRODUCE, from rank-1 minor conditions,
the two-term decomposition equations that AO2016 derived BY HAND
(rank-2 H = α₁H₁ₛ + α₂H₂; H₁ₛ symmetric, H₂ free) — then (A9-A10) generalization and the rank-3
discovery region.

**Convention warning (critical)**: AO2016 defines covariance in the STANDARD basis:
H = ¼Σ mᵢⱼ(σᵢ⊗σⱼ), mᵢⱼ = tr[(σᵢ⊗σⱼ)H] (Eq. 2-3) — a DIFFERENT object from the
Π-basis `covariance_from_mueller` in the core. The decomposition module carries its own
standard-basis conversion; the two bases must not be mixed (separated by test).

## 2. Goals

1. **`decomposition/` package**:
   - `covariance.py`: standard-basis H↔M conversions; Type 1/2/3 H-templates
     (Table 1) as parameter functions + template→parameter extraction.
   - `derive.py`: **DERIVER** — over generic Hermitian H symbols
     build the selected 2×2 minors of the residual matrix (H − α₁H₁ₛ), solve with SymPy,
     PRODUCE closed-form equations; compare SYMBOLICALLY one-to-one against the paper's
     Table 2 formulas (hand-entered).
   - `solve.py`: numeric solver — M (or H) + assumed type → α₁, H₁ₛ,
     H₂, M₁, M₂; applicability guards (rank-2, relevant determinant
     not ≈0, weight ∈ (0,1), eigen-physicality) — on violation an explicit error,
     NO silent result (user directive: guards).
2. **Scope this stage**: Type 1 (two variants), Type 2a/2b, Type 3a/3b —
   the entirety of Table 2. Table 4 (Type 1-2/1-3/2-3) → A9.
3. **Acceptance**:
   - A: Derived equations ≡ Table 2 (symbolic, per type).
   - B: **Paper §6 numeric example one-to-one**: M₁ (Eq. 16a, type-3) + M₂
     (16b), α=0.3/0.7 → solver must return α₁E=0.1433, α₁V=0.0289+0.0112i,
     α₁Ē=0.0067, α₁=0.3, H₁ (Eq. 21, 4 decimals).
   - C: Synthetic roundtrip: random type-k pure + random pure, random
     weight → two components + weight recovered (3 types × 2 variants,
     deterministic seed).
   - D: Degenerate case (two components same symmetry) guard gives an explicit error
     (paper: "overlap makes the decomposition impossible").
   - E: Existing 92 tests green.
4. **`docs/design-note-guarded-atoms.md`**: DESIGN of conditional atom classes
   (implementation A9+): guards enter the INTERPRETATION layer, not the AXIOM layer
   (constrained generators) — soundness cost zero; guard-correct-but-unproven
   pairs fall into the `underivable` channel with a guard tag = Horn-conditional
   identity candidates. Per K24, the axiom side is not opened without auditor approval.

## 3. Architectural decisions

- **M28. Deriver ≠ table copy**: the equations are produced from minor conditions by SymPy
  solution; the hand-entered Table 2 is only a COMPARISON anchor.
- **M29. Standard-basis covariance lives in the decomposition module**; the core Π-basis
  is unchanged (K11).
- **M30. OCR unreliability**: there may be overbar losses in the paper text; the final
  arbiter = the triple of symbolic derivation + §6 numeric anchor + synthetic roundtrip.

## 4. Strict rules

K26. The solver throws an exception in an inapplicable state (silent NaN/wrong result forbidden).
K27. All numeric tests are deterministically seeded.
K28. A simplification failure in a table comparison = stage failed
(no glossing over with approximate equality; the symbolic difference must be exactly zero).

## 5-6. Delivery + Verification

`decomposition/{__init__,covariance,templates,derive,solve}.py` ·
`tests/test_decomposition.py` · design note · report. Acceptance A-E.

## 7-9.

Push + report + A9 (5 min). Warning: the paper's H₁ normalization is tr=1;
weight α₁ = tr(α₁H₁ₛ) is x+w·w̄/x in type-1, 2(k+k̄) in type-2/3. Out of scope:
Table 4 types (A9), rank-3 (A10), experimental data handling, Cloude-cutoff.

**STOP HERE**
