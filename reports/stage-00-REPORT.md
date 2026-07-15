# STAGE 0 — REPORT

**Date**: 2026-07-13
**Spec**: `specs/stage-00.md`
**Result**: COMPLETED — acceptance criterion met (14/14 known identities recovered, 36/36 tests green)

---

## 1. Deliverables

- Repo skeleton: `specs/`, `reports/`, `src/organon_mueller/`, `tests/`, `.github/workflows/ci.yml`, `pyproject.toml`, `.gitignore`, README.
- **Representation layer** (`algebra/`): six isomorphic representations — Jones J, Mueller M, covariance matrix H, covariance vector |h⟩=(τ,α,β,γ), Z matrix, h biquaternion — and all conversions. Source representation |h⟩ (decision M1). Conventions fixed to the Kuntman-Arteaga papers (decision M5).
- **Biquaternion algebra** (`algebra/quaternion.py`): Hamilton product, two conjugates (bar and †), 4×4 matrix representation (overlaps with Z — symbolically proven homomorphism).
- **Known-identity library** (`identities/known.py`): 14 identities, each with source + side condition (guard) + verification mode metadata. `verify_all()` runs them all in a single call.
- **Predicate layer seed** (`conditions.py`): `CONDITIONS` dictionary (nondepolarizing, det_nonzero, hermitian_state, unitary_state) — the first form of the Horn-conditioned rule infrastructure (decision M3); the condition keys in the identity records were bound to this dictionary by test.
- **Verification helpers** (`verify.py`): symbolic (expand-based, exact for polynomial identities) + deterministic numerical sampling (seed=20260713, decision M2/K2).
- **Literature anchors** (`tests/test_fixtures.py`): horizontal/vertical polarizer, quarter-wave plate, rotator state — external anchor tests fixed with hand-derived expected Mueller entries.

## 2. Verification results

- `pytest`: **36/36 green** (~15 s). Spec §6 list I1–I14: **14/14 recovered** (I1–I5, I7, I8 symbolic-exact; I6, I9, I11–I14 numeric-deterministic; I10 symbolic+numeric).
- CI: GitHub Actions, Python 3.10/3.11/3.12 matrix — will run on first push.

## 3. Independent audit (adversarial review)

An auditor agent that did not write the implementation recomputed and verified 7 identities via **independent routes** from the paper formulas (e.g. the M_ij = ½tr(σᵢJσⱼJ†) route, hand-written quaternion product, coherence-matrix route ρ′=JρJ†). Verdict: **PASS**. Findings and actions taken:

| Finding | Action |
|---|---|
| `hvector_from_covariance` silently returns a zero state at τ=0 | ✅ ValueError guard added + regression test |
| Report file missing | ✅ this file |
| Route-to-route tests can hide a correlated convention error | ✅ 4 literature anchor tests added |
| `det_nonzero` condition key has no corresponding predicate | ✅ `has_nonzero_det_params` + `CONDITIONS` dictionary + verifying test |
| CI does not test the 3.10 baseline | ✅ 3.10 added to the matrix |
| Input hygiene (raw float/wrong type) | ✅ `__post_init__` sympify + `__mul__` NotImplemented |
| I9's matrix leg is semi-tautological (already follows from the homomorphism) | ℹ️ Noted; the load-bearing leg (quaternion sandwich vs M|s⟩) is independent. No change needed |

## 4. Decisions and open questions

1. **LICENSE**: deliberately not added — the MIT/Apache choice is a user decision (repo private, no urgency). → *Open question #1*
2. **egglog**: absent at this stage (decision M6). A small spike before Stage 2 (how to encode complex-valued, noncommutative matrix algebra in egglog) is essential.
3. **τ=0 symmetry classes** (half-wave plate type states): left out of `hvector_from_covariance` scope, protected by a guard. To be generalized later with Class-1 generators. → *Open question #2*
4. Stokes samples contain non-physical vectors for algebraic purposes (the s₀² ≥ s₁²+s₂²+s₃² condition is not required) — a deliberate choice, since the identities hold over all of ℝ⁴.

## 5. Next stage proposal

**Stage 1 — Identity library expansion + serialization**: the coherent superposition identities from PRA 95,063819 (Z = aZ_a + bZ_b, coherence terms) and the Type 1/2/3 symmetry-covariance relations of Applied Optics 2016 (Table 1) are added to the library; JSON/string serialization of the expressions (MCP-preparation, decision M4) is written. In parallel, the **egglog spike** (time-boxed, its result shapes the Stage 2 spec).

## 6. Proposed commit

```
git add -A
git commit -m "Stage 0: representation layer + known-identity regression core

- Six isomorphic representations (J, M, H, |h>, Z, biquaternion) with conversions
- Known-identity library: 14 identities recovered (symbolic + deterministic numeric)
- Condition predicate seed (Horn guards), literature fixtures, CI (py3.10-3.12)
- Independently reviewed (adversarial pass): tau=0 guard, external anchors added"
git push
```
